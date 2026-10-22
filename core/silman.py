"""Playable lessons from Silman's Complete Endgame Course."""

from core.primer import _lesson
from core.silman_course import COURSE
from core.silman_study import PARTS, part_label, pdf_page


def lessons():
    built = tuple(_lesson(spec) for spec in COURSE)
    if [lesson.id for lesson in built] != [spec["id"] for spec in COURSE]:
        raise RuntimeError("Silman lessons were not loaded in book order.")
    return built


__all__ = ["PARTS", "lessons", "part_label", "pdf_page"]
