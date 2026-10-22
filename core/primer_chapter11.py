"""Appendix board tasks; chapter11 is displayed to learners as Appendix."""
from core.primer_build import lesson, step
from core.primer_guides_chapter11 import EXERCISES

LESSONS = [
    lesson(11, item['id'], item['title'], item['summary'],
           [step(item['fen'], item['inventory']), step(item['fen'], item['prompt'])],
           item['prompt'], item['choices'], objective=item.get('objective'))
    for item in EXERCISES
]
