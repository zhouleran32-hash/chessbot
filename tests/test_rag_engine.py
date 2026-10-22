"""Real PDF extraction and persistent vector retrieval with offline embeddings."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from langchain_core.embeddings import Embeddings
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from core.rag_engine import ChessBookKnowledgeBase, KnowledgeBaseError, PDFIngestionError


class OfflineEmbeddings(Embeddings):
    """Known vectors make the retrieval order independently predictable."""

    model = "offline-test-v1"

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        text = text.lower()
        if any(word in text for word in ("queen", "royal lady")):
            return [1.0, 0.0, 0.0, 0.0]
        if any(word in text for word in ("castle", "king", "monarch")):
            return [0.0, 1.0, 0.0, 0.0]
        if any(word in text for word in ("hanging", "undefended", "loose")):
            return [0.0, 0.0, 1.0, 0.0]
        return [0.0, 0.0, 0.0, 1.0]


def write_pdf(path, pages):
    """Create a tiny text PDF fixture without an extra authoring dependency."""
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    }))
    for text in pages:
        page = writer.add_blank_page(width=612, height=792)
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font}),
        })
        commands = ["BT /F1 12 Tf 50 740 Td 16 TL"]
        for line in text.splitlines():
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(f"({escaped}) Tj T*")
        commands.append("ET")
        stream = DecodedStreamObject()
        stream.set_data("\n".join(commands).encode("ascii"))
        page[NameObject("/Contents")] = writer._add_object(stream)
    with path.open("wb") as destination:
        writer.write(destination)


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = self.root / "chroma"
        self.pdf = self.root / "strategy.pdf"
        write_pdf(self.pdf, [
            "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6\n4. Ba4 Nf6 5. O-O Be7 6. Re1 b5",
            "Do not bring the queen out too early. Develop minor pieces first to avoid losing time.\n1. e4 e5 2. Qh5 Nc6 3. Qxe5+ Nxe5",
            "Castle early to protect your king. Keep a shelter of pawns around it.",
        ])

    def knowledge_base(self, **kwargs):
        kwargs.setdefault("embeddings", OfflineEmbeddings())
        if kwargs["embeddings"] is not None:
            kwargs.setdefault("embedding_id", kwargs["embeddings"].model)
        return ChessBookKnowledgeBase(persist_directory=self.store, **kwargs)

    def test_empty_library_uses_ten_in_memory_principles_without_an_api_key(self):
        with patch("core.rag_engine.OpenAIEmbeddings", side_effect=AssertionError("No network model needed")):
            kb = self.knowledge_base(embeddings=None, openai_api_key="")
            advice = kb.search_advice("queen out early", n_results=100)
        self.assertEqual(len(advice), 10)
        self.assertEqual(len(set(advice)), 10)
        self.assertIn("queen", advice[0].lower())
        self.assertTrue(all("Built-in beginner principles" in item for item in advice))
        self.assertTrue(all("page n/a" in item for item in advice))

    def test_seed_search_ranks_hanging_piece_advice_and_honors_count(self):
        advice = self.knowledge_base().search_advice("hanging undefended pieces", 1)
        self.assertEqual(len(advice), 1)
        self.assertIn("loose pieces drop off", advice[0].lower())

    def test_real_pdf_ingestion_removes_notation_and_retains_source_page(self):
        kb = self.knowledge_base()
        self.assertEqual(kb.ingest_pdf(str(self.pdf)), 2)
        advice = kb.search_advice("royal lady", 10)
        self.assertEqual(len(advice), 2)
        self.assertIn("Do not bring the queen", advice[0])
        self.assertIn("[Source: strategy.pdf | page 2]", advice[0])
        self.assertIn("[Source: strategy.pdf | page 3]", advice[1])
        self.assertFalse(any("1. e4" in item or "Built-in" in item for item in advice))
        self.assertTrue((self.store / "chroma.sqlite3").is_file())

    def test_vector_search_matches_a_concept_without_matching_query_words(self):
        kb = self.knowledge_base()
        kb.ingest_pdf(str(self.pdf))
        advice = kb.search_advice("monarch sanctuary", 1)
        self.assertIn("Castle early", advice[0])
        self.assertIn("page 3", advice[0])

    def test_reopening_the_persistent_library_preserves_advice(self):
        original = self.knowledge_base()
        original.ingest_pdf(str(self.pdf))
        expected = original.search_advice("royal lady", 1)
        reopened = self.knowledge_base()
        self.assertEqual(reopened.search_advice("royal lady", 1), expected)

    def test_reingesting_the_same_pdf_does_not_duplicate_chunks(self):
        kb = self.knowledge_base()
        self.assertEqual(kb.ingest_pdf(str(self.pdf)), 2)
        self.assertEqual(kb.ingest_pdf(str(self.pdf)), 2)
        self.assertEqual(len(kb.search_advice("opening principles", 100)), 2)

    def test_custom_collection_is_selected_and_can_be_reopened(self):
        kb = self.knowledge_base()
        kb.ingest_pdf(str(self.pdf), collection_name="opening_books")
        self.assertIn("strategy.pdf", kb.search_advice("queen", 1)[0])
        reopened = self.knowledge_base(collection_name="opening_books")
        self.assertIn("strategy.pdf", reopened.search_advice("queen", 1)[0])
        self.assertIn("Built-in beginner principles", self.knowledge_base().search_advice("queen", 1)[0])

    def test_long_prose_is_split_into_bounded_chunks(self):
        prose = "Develop knights and bishops early. Control central squares before attacking. " * 30
        write_pdf(self.pdf, [prose])
        kb = self.knowledge_base()
        count = kb.ingest_pdf(str(self.pdf))
        self.assertGreater(count, 3)
        snippets = kb.search_advice("central squares", 100)
        self.assertEqual(len(snippets), count)
        self.assertTrue(all(len(item.split("\n\n[Source:")[0]) <= 600 for item in snippets))

    def test_short_explanations_with_moves_are_preserved(self):
        write_pdf(self.pdf, [
            "After 1. e4, control the center with pawns.\n2. Nf3 develops a knight toward the center.",
        ])
        kb = self.knowledge_base()
        self.assertGreater(kb.ingest_pdf(str(self.pdf)), 0)
        advice = kb.search_advice("center", 3)
        self.assertIn("control the center with pawns", advice[0])
        self.assertIn("develops a knight", advice[0])

    def test_short_explanation_after_a_long_variation_is_preserved(self):
        write_pdf(self.pdf, [
            "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 Develop pieces.\n"
            "1. d4 d5 2. c4 e6 3. Nc3 Nf6 4. Bg5 Be7 Black equalizes.",
        ])
        kb = self.knowledge_base()
        self.assertEqual(kb.ingest_pdf(str(self.pdf)), 1)
        advice = kb.search_advice("development", 1)[0]
        self.assertIn("Develop pieces.", advice)
        self.assertIn("Black equalizes.", advice)
        self.assertNotIn("1. e4", advice)
        self.assertNotIn("1. d4", advice)

    def test_only_move_notation_needs_no_embeddings_and_keeps_seed_fallback(self):
        notation = "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6\n4...Nf6 5.O-O Be7 6.Re1 b5 1-0"
        write_pdf(self.pdf, [notation])
        with patch("core.rag_engine.OpenAIEmbeddings", side_effect=AssertionError("No embeddings needed")):
            kb = self.knowledge_base(embeddings=None, openai_api_key="")
            self.assertEqual(kb.ingest_pdf(str(self.pdf)), 0)
            self.assertIn("Built-in beginner principles", kb.search_advice("center", 1)[0])

    def test_blank_pdf_returns_zero_chunks(self):
        write_pdf(self.pdf, [""])
        self.assertEqual(self.knowledge_base().ingest_pdf(str(self.pdf)), 0)

    def test_missing_or_invalid_pdf_has_a_clear_error(self):
        kb = self.knowledge_base()
        with self.assertRaises(FileNotFoundError):
            kb.ingest_pdf(str(self.root / "missing.pdf"))
        text_file = self.root / "notes.txt"
        text_file.write_text("Control the center.")
        with self.assertRaises(ValueError):
            kb.ingest_pdf(str(text_file))
        self.pdf.write_bytes(b"not a valid PDF")
        with self.assertRaises(PDFIngestionError):
            kb.ingest_pdf(str(self.pdf))

    def test_missing_api_key_is_reported_for_real_book_ingestion(self):
        kb = self.knowledge_base(embeddings=None, openai_api_key="")
        with self.assertRaisesRegex(KnowledgeBaseError, "OPENAI_API_KEY"):
            kb.ingest_pdf(str(self.pdf))

    def test_default_embedding_provider_is_created_lazily_with_the_configured_key(self):
        with patch("core.rag_engine.OpenAIEmbeddings", return_value=OfflineEmbeddings()) as factory:
            kb = self.knowledge_base(embeddings=None, openai_api_key="test-key")
            factory.assert_not_called()
            kb.ingest_pdf(str(self.pdf))
            self.assertEqual(factory.call_args.kwargs["api_key"], "test-key")
            self.assertEqual(factory.call_args.kwargs["model"], "text-embedding-3-small")
            self.assertIn("Castle early", kb.search_advice("monarch sanctuary", 1)[0])

    def test_embedding_failure_is_reported_and_does_not_claim_ingestion_success(self):
        class FailingEmbeddings(OfflineEmbeddings):
            def embed_documents(self, texts):
                raise ConnectionError("provider offline")

        kb = self.knowledge_base(embeddings=FailingEmbeddings())
        with self.assertRaisesRegex(KnowledgeBaseError, "[Ee]mbedding"):
            kb.ingest_pdf(str(self.pdf))
        self.assertIn("Built-in beginner principles", kb.search_advice("center", 1)[0])

    def test_embedding_model_mismatch_is_rejected_before_querying(self):
        self.knowledge_base().ingest_pdf(str(self.pdf))

        class DifferentEmbeddings(OfflineEmbeddings):
            model = "different-model"

        with self.assertRaisesRegex(KnowledgeBaseError, "[Ee]mbedding"):
            self.knowledge_base(embeddings=DifferentEmbeddings()).search_advice("queen")

    def test_custom_provider_requires_an_explicit_vector_space_identity(self):
        with self.assertRaisesRegex(ValueError, "embedding_id"):
            ChessBookKnowledgeBase(persist_directory=self.store, embeddings=OfflineEmbeddings())

    def test_custom_provider_model_change_is_rejected_for_search_and_ingestion(self):
        class ConfiguredEmbeddings(Embeddings):
            def __init__(self, model_name):
                self.model_name = model_name

            def embed_documents(self, texts):
                return [self.embed_query(text) for text in texts]

            def embed_query(self, text):
                vector = OfflineEmbeddings().embed_query(text)
                if self.model_name == "model-b":
                    vector[0], vector[1] = vector[1], vector[0]
                return vector

        first = ChessBookKnowledgeBase(
            persist_directory=self.store,
            embeddings=ConfiguredEmbeddings("model-a"), embedding_id="configured:model-a:v1",
        )
        first.ingest_pdf(str(self.pdf))
        self.assertIn("Do not bring the queen", first.search_advice("queen", 1)[0])
        second = ChessBookKnowledgeBase(
            persist_directory=self.store,
            embeddings=ConfiguredEmbeddings("model-b"), embedding_id="configured:model-b:v1",
        )
        with self.assertRaises(KnowledgeBaseError):
            second.search_advice("queen", 1)
        with self.assertRaises(KnowledgeBaseError):
            second.ingest_pdf(str(self.pdf))
        self.assertIn("Do not bring the queen", first.search_advice("queen", 1)[0])

    def test_invalid_search_arguments_and_zero_results(self):
        kb = self.knowledge_base()
        self.assertEqual(kb.search_advice("queen", 0), [])
        for query in ("", " ", None):
            with self.subTest(query=query), self.assertRaises(ValueError):
                kb.search_advice(query)
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                kb.search_advice("queen", count)

    def test_storage_errors_are_not_disguised_as_an_empty_library(self):
        blocked_path = self.root / "not_a_directory"
        blocked_path.write_text("occupied")
        kb = ChessBookKnowledgeBase(
            persist_directory=blocked_path, embeddings=OfflineEmbeddings(), embedding_id="offline-test-v1",
        )
        with self.assertRaises(KnowledgeBaseError):
            kb.search_advice("queen")


if __name__ == "__main__":
    unittest.main()
