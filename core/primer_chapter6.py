"""Playable Chapter 6 lessons; the full authored teaching lives in its guide module."""
from core.primer_build import lesson, step
from core.primer_guides_chapter6 import EXERCISES

LESSONS = [
    lesson(6, item['id'], item['title'], item['summary'],
           [step(item['fen'], item['inventory']), step(item['fen'], item['prompt'])],
           item['prompt'], item['choices'], objective=item.get('objective'))
    for item in EXERCISES
]
