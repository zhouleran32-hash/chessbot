"""Board exercises for the opening-theory chapter."""
from core.primer_build import lesson, step
from core.primer_guides_chapter10 import EXERCISES

LESSONS = [
    lesson(10, item['id'], item['title'], item['summary'],
           [step(item['fen'], item['inventory']), step(item['fen'], item['prompt'])],
           item['prompt'], item['choices'], objective=item.get('objective'))
    for item in EXERCISES
]
