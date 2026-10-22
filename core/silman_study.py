"""Syllabus map for Silman's Complete Endgame Course.

Printed pages are the book's own numbers. In this scan, PDF page = printed page + 14
(printed page 7 is PDF page 21). Front matter uses roman numerals and a different offset.
"""

from core.primer_study import example_frames


PDF_PAGE_OFFSET = 14

PARTS = {
    1: ("Endgames for beginners", "Unrated–999", 1, 30),
    2: ("Endgames for class E", "1000–1199", 31, 54),
    3: ("Endgames for class D", "1200–1399", 55, 88),
    4: ("Endgames for class C", "1400–1599", 89, 158),
    5: ("Endgames for class B", "1600–1799", 159, 212),
    6: ("Endgames for class A", "1800–1999", 213, 270),
    7: ("Endgames for experts", "2000–2199", 271, 346),
    8: ("Endgames for masters", "2200–2399", 347, 428),
    9: ("Endgames for pure pleasure", "Studies and master games", 429, 524),
}


def part_label(number: int) -> str:
    title, band, _start, _end = PARTS[number]
    return f"Part {number} · {title} ({band})"


def pdf_page(printed: int) -> int:
    return printed + PDF_PAGE_OFFSET


def points(text):
    """Keep one markdown line per source line. Blank lines are dropped."""
    return "\n".join(line.strip() for line in text.strip().splitlines() if line.strip())


def point_lesson(chapter, lesson_id, title, explanation, steps, prompt, choices, *, objective=None):
    from core.primer_build import lesson as build_lesson

    spec = build_lesson(chapter, lesson_id, title, "placeholder", steps, prompt, choices, objective=objective)
    spec["explanation"] = points(explanation)
    return spec


def section(title, body):
    return {"title": title, "body": " ".join(body.split())}


def example(title, fen, moves, notes):
    return {"title": title, "fen": fen, "moves": tuple(moves), "notes": tuple(notes)}


def check(check_id, prompt, *options):
    return {"id": check_id, "prompt": prompt, "options": tuple(
        {"text": text, "correct": correct, "explanation": explanation}
        for text, correct, explanation in options
    )}


def guide(pages, goals, sections, examples, pitfalls, checks, recap):
    return dict(pages=pages, goals=tuple(goals), sections=tuple(sections),
                examples=tuple(examples), pitfalls=tuple(pitfalls),
                checks=tuple(checks), recap=tuple(recap))


def guide_for(lesson_id: str) -> dict | None:
    from core.silman_guides_chapter1 import GUIDES as PART_ONE
    from core.silman_guides_chapter2 import GUIDES as PART_TWO
    from core.silman_guides_chapter3 import GUIDES as PART_THREE
    from core.silman_guides_chapter4 import GUIDES as PART_FOUR
    from core.silman_guides_chapter5 import GUIDES as PART_FIVE
    from core.silman_guides_chapter6 import GUIDES as PART_SIX
    from core.silman_guides_chapter7 import GUIDES as PART_SEVEN
    from core.silman_guides_chapter8 import GUIDES as PART_EIGHT
    from core.silman_guides_chapter9 import GUIDES as PART_NINE

    return {**PART_ONE, **PART_TWO, **PART_THREE, **PART_FOUR, **PART_FIVE, **PART_SIX, **PART_SEVEN, **PART_EIGHT, **PART_NINE}.get(lesson_id)


def validate_guide(guide_data: dict, part: int) -> None:
    start, end = guide_data["pages"]
    _title, _band, part_start, part_end = PARTS[part]
    if not part_start <= start <= end <= part_end:
        raise ValueError("Guide pages must lie inside the cited part's printed page range.")
    if not guide_data["goals"] or not guide_data["sections"] or not guide_data["examples"] or not guide_data["checks"] or not guide_data["recap"]:
        raise ValueError("A guide needs goals, explanations, worked examples, questions, and a recap.")
    for item in guide_data["sections"]:
        if not item["title"].strip() or not item["body"].strip():
            raise ValueError("Every explanation section needs a title and text.")
    for item in guide_data["examples"]:
        example_frames(item)
    seen = set()
    for question in guide_data["checks"]:
        if question["id"] in seen:
            raise ValueError("Concept-check IDs must be unique within a lesson.")
        seen.add(question["id"])
        if sum(option["correct"] is True for option in question["options"]) != 1:
            raise ValueError("Each concept question must have exactly one correct answer.")
        if not question["prompt"].strip() or any(not option["text"].strip() or not option["explanation"].strip() for option in question["options"]):
            raise ValueError("Every concept option needs its own explanation.")
