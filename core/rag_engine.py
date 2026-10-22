"""Persistent chess-book retrieval with a small, API-free beginner fallback."""

import hashlib
from pathlib import Path
import re

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.errors import NotFoundError
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import load_config


class KnowledgeBaseError(RuntimeError):
    """The embedding provider or local knowledge store could not be used."""


class PDFIngestionError(KnowledgeBaseError):
    """A PDF could not be read and prepared for ingestion."""


class ChessBookKnowledgeBase:
    """Index explanatory book passages and retrieve cited text snippets.

    Book search uses OpenAI embeddings by default. Inject a LangChain Embeddings
    instance with a stable embedding_id to use another provider. The ten seed
    principles stay in memory and are ranked by keywords when the active
    collection has no book chunks; that
    fallback never needs an API key or an embedding-model download.
    """

    SEED_PRINCIPLES = (
        "Control the center with pawns and support them with your pieces.",
        "Develop your knights and bishops early so they influence important squares.",
        "Do not bring the queen out too early; attacks on it can cost development time.",
        "Castle within the first ten moves when it is safe, bringing your king to shelter.",
        "Never leave pieces undefended: loose pieces drop off. Check for hanging pieces before moving.",
        "Before every move, check your opponent's checks, captures, and threats, including forks, pins, and skewers.",
        "Protect your king and avoid weakening the pawns around it.",
        "Avoid moving the same piece repeatedly in the opening without a concrete reason.",
        "Connect your rooks and place them on open or semi-open files.",
        "When ahead in material, consider trading pieces while preserving your advantage.",
    )
    MOVE_TOKEN = re.compile(
        r"(?:[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=?[QRBN])?|[O0]-[O0](?:-[O0])?)[+#]?[!?]*"
    )
    MOVE_NUMBER = re.compile(r"\b\d+\.(?:\.\.)?")
    RESULT_TOKEN = re.compile(r"^(?:1-0|0-1|1/2-1/2|½-½|\*|\$\d+)$")

    def __init__(
        self,
        persist_directory: str | Path | None = None,
        *,
        collection_name: str = "chess_books",
        embeddings: Embeddings | None = None,
        embedding_id: str | None = None,
        openai_api_key: str | None = None,
        embedding_model: str = "text-embedding-3-small",
    ):
        config = load_config()
        self.persist_directory = (
            Path(persist_directory).expanduser().resolve()
            if persist_directory is not None else config.chroma_dir
        )
        self.collection_name = self._validate_collection_name(collection_name)
        self.embedding_model = embedding_model
        self._embeddings = embeddings
        self._api_key = config.openai_api_key if openai_api_key is None else openai_api_key
        if embeddings is not None:
            if not isinstance(embedding_id, str) or not embedding_id.strip():
                raise ValueError(
                    "Supply embedding_id for custom embeddings, identifying their "
                    "provider, model, dimensions, and vector-affecting configuration."
                )
            self._embedding_id = f"custom:{embedding_id.strip()}"
        else:
            if embedding_id is not None:
                raise ValueError("embedding_id is only used with a custom embeddings provider")
            self._embedding_id = f"openai:{embedding_model}"
        self._client = None

    def ingest_pdf(self, pdf_path: str, collection_name: str = "chess_books") -> int:
        """Store explanatory chunks and select this collection for future searches.

        Returns the number of eligible chunks processed, including existing
        chunks refreshed by an identical import. Blank or notation-only PDFs
        return zero. Page citations use one-based PDF page numbers.
        """
        name = self._validate_collection_name(collection_name)
        path = Path(pdf_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"PDF not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError("Choose a .pdf file to ingest")
        try:
            pages = PyPDFLoader(str(path)).load()
            chunks = RecursiveCharacterTextSplitter(
                chunk_size=600, chunk_overlap=80
            ).split_documents(pages)
            digest = hashlib.sha256()
            with path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(block)
        except Exception as exc:
            raise PDFIngestionError(
                f"Could not read PDF '{path.name}'. Check that it is a readable, unencrypted PDF."
            ) from exc

        book_id = digest.hexdigest()
        records = []
        for index, chunk in enumerate(chunks):
            text = self._concept_text(chunk.page_content)
            if not text:
                continue
            page = int(chunk.metadata["page"]) + 1
            identity = f"{book_id}:{page}:{index}:{text}"
            records.append((hashlib.sha256(identity.encode()).hexdigest(), text, {
                "source_book": path.name,
                "source_path": str(path),
                "page": page,
                "book_id": book_id,
                "chunk_index": index,
            }))

        if not records:
            self.collection_name = name
            return 0
        collection = self._get_collection(name, create=True)
        self._check_embedding_identity(collection)
        provider = self._get_embeddings()
        batch_size = min(256, self._get_client().get_max_batch_size())
        for offset in range(0, len(records), batch_size):
            batch = records[offset:offset + batch_size]
            documents = [record[1] for record in batch]
            try:
                vectors = provider.embed_documents(documents)
            except Exception as exc:
                raise KnowledgeBaseError(
                    "Could not create text embeddings. Check the embedding provider, "
                    "OPENAI_API_KEY, connectivity, and API limits."
                ) from exc
            try:
                collection.upsert(
                    ids=[record[0] for record in batch],
                    documents=documents,
                    embeddings=vectors,
                    metadatas=[record[2] for record in batch],
                )
            except Exception as exc:
                raise KnowledgeBaseError("Could not store book chunks in local Chroma storage.") from exc
        self.collection_name = name
        return len(records)

    def search_advice(self, query_concept: str, n_results: int = 3) -> list[str]:
        """Return semantic matches with source/page citations, or built-in advice."""
        if not isinstance(query_concept, str) or not query_concept.strip():
            raise ValueError("query_concept must be a non-empty string")
        if isinstance(n_results, bool) or not isinstance(n_results, int) or n_results < 0:
            raise ValueError("n_results must be a non-negative integer")
        if n_results == 0:
            return []
        collection = self._get_collection(self.collection_name, create=False)
        try:
            count = collection.count() if collection is not None else 0
        except Exception as exc:
            raise KnowledgeBaseError("Could not read the local Chroma collection.") from exc
        if count == 0:
            return self._seed_advice(query_concept, n_results)

        self._check_embedding_identity(collection)
        provider = self._get_embeddings()
        try:
            vector = provider.embed_query(query_concept.strip())
        except Exception as exc:
            raise KnowledgeBaseError(
                "Could not embed the advice query. Check the embedding provider, "
                "OPENAI_API_KEY, connectivity, and API limits."
            ) from exc
        try:
            result = collection.query(
                query_embeddings=[vector],
                n_results=min(n_results, count),
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            raise KnowledgeBaseError("Could not search the local Chroma collection.") from exc
        return [
            f"{text}\n\n[Source: {metadata['source_book']} | page {metadata['page']}]"
            for text, metadata in zip(result["documents"][0], result["metadatas"][0])
        ]

    def _get_client(self):
        if self._client is None:
            try:
                self.persist_directory.mkdir(parents=True, exist_ok=True)
                self._client = chromadb.PersistentClient(
                    path=str(self.persist_directory),
                    settings=ChromaSettings(anonymized_telemetry=False),
                )
            except Exception as exc:
                raise KnowledgeBaseError(
                    f"Could not open local Chroma storage at '{self.persist_directory}'."
                ) from exc
        return self._client

    def _get_collection(self, name: str, *, create: bool):
        client = self._get_client()
        try:
            if create:
                return client.get_or_create_collection(
                    name=name,
                    embedding_function=None,
                    metadata={"embedding_id": self._embedding_id},
                    configuration={"hnsw": {"space": "cosine"}},
                )
            return client.get_collection(name=name, embedding_function=None)
        except NotFoundError:
            if not create:
                return None
            raise KnowledgeBaseError(f"Could not create Chroma collection '{name}'.")
        except Exception as exc:
            raise KnowledgeBaseError(f"Could not open Chroma collection '{name}'.") from exc

    def _get_embeddings(self) -> Embeddings:
        if self._embeddings is None:
            if not self._api_key or not self._api_key.strip():
                raise KnowledgeBaseError(
                    "Set OPENAI_API_KEY in .env to embed and search book passages, "
                    "or supply an embeddings provider. Built-in advice works without a key."
                )
            self._embeddings = OpenAIEmbeddings(
                model=self.embedding_model,
                api_key=self._api_key,
                timeout=30,
                max_retries=2,
                check_embedding_ctx_length=False,
            )
        return self._embeddings

    def _check_embedding_identity(self, collection) -> None:
        if (collection.metadata or {}).get("embedding_id") != self._embedding_id:
            raise KnowledgeBaseError(
                "Embedding provider/model differs from the one used for this collection. "
                "Use the original embeddings or ingest into a new collection."
            )

    @staticmethod
    def _validate_collection_name(name: str) -> str:
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,510}[A-Za-z0-9]", name):
            raise ValueError("collection_name must be 3-512 letters, digits, dots, underscores, or hyphens, starting and ending with a letter or digit")
        return name

    @classmethod
    def _concept_text(cls, text: str) -> str:
        """Keep prose; remove pure move lists and trim notation-heavy examples.

        This heuristic preserves explanatory sentences containing SAN. Scanned
        pages need OCR before ingestion; no image-to-text conversion is attempted.
        """
        kept = []
        for line in text.splitlines():
            cleaned = cls.MOVE_NUMBER.sub(" ", line)
            tokens = [token.strip(".,;:()[]{}\"'") for token in cleaned.split()]
            tokens = [token for token in tokens if token and not cls.RESULT_TOKEN.fullmatch(token)]
            moves = sum(bool(cls.MOVE_TOKEN.fullmatch(token)) for token in tokens)
            prose = [
                token for token in tokens
                if not cls.MOVE_TOKEN.fullmatch(token)
                and len(token) >= 2
                and re.fullmatch(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", token)
            ]
            if not prose:
                continue
            if moves and moves / (moves + len(prose)) >= 0.8:
                explanation = []
                for token in cleaned.split():
                    normalized = token.strip(".,;:()[]{}\"'")
                    if not cls.MOVE_TOKEN.fullmatch(normalized) and not cls.RESULT_TOKEN.fullmatch(normalized):
                        explanation.append(token)
                kept.append(" ".join(explanation))
            else:
                kept.append(line.strip())
        return "\n".join(kept).strip()

    @classmethod
    def _seed_advice(cls, query: str, count: int) -> list[str]:
        stopwords = {"the", "a", "an", "and", "to", "of", "with", "on", "in", "your", "it", "or", "for"}
        query_words = set(re.findall(r"[a-z]+", query.lower())) - stopwords
        ranked = sorted(
            enumerate(cls.SEED_PRINCIPLES),
            key=lambda item: (-len(query_words & set(re.findall(r"[a-z]+", item[1].lower()))), item[0]),
        )
        return [
            f"{text}\n\n[Source: Built-in beginner principles | page n/a]"
            for _, text in ranked[:count]
        ]
