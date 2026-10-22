"""Combined primer syllabus for chapters 1–10 and the appendix."""

from core.primer_chapter1 import LESSONS as CHAPTER_1
from core.primer_chapter2 import LESSONS as CHAPTER_2
from core.primer_chapter3 import LESSONS as CHAPTER_3
from core.primer_chapter4 import LESSONS as CHAPTER_4
from core.primer_chapter5 import LESSONS as CHAPTER_5
from core.primer_chapter6 import LESSONS as CHAPTER_6
from core.primer_chapter7 import LESSONS as CHAPTER_7
from core.primer_chapter8 import LESSONS as CHAPTER_8
from core.primer_chapter9 import LESSONS as CHAPTER_9
from core.primer_chapter10 import LESSONS as CHAPTER_10
from core.primer_chapter11 import LESSONS as APPENDIX

COURSE = [*CHAPTER_1, *CHAPTER_2, *CHAPTER_3, *CHAPTER_4, *CHAPTER_5,
          *CHAPTER_6, *CHAPTER_7, *CHAPTER_8, *CHAPTER_9, *CHAPTER_10, *APPENDIX]
