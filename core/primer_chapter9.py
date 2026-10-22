"""Playable Chapter 9 exercises paired with the detailed middlegame guides."""
from core.primer_build import lesson, step
from core.primer_guides_chapter9 import GUIDES, LESSON_DATA

LESSONS = [lesson(9, item['id'], item['title'], item['explanation'],
                  [step(item['fen'], GUIDES[item['id']]['examples'][0]['notes'][0]),
                   step(item['fen'], 'Your task: ' + item['prompt'])], item['prompt'],
                  item['choices'], objective=item['objective'])
           for item in LESSON_DATA]
