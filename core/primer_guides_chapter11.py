"""Appendix guides, ordered as foundations, problems, then studies."""
from core.primer_appendix_foundations import GUIDES as FOUNDATIONS, EXERCISES as FOUNDATION_TASKS
from core.primer_appendix_two import GUIDES as TWO_MOVERS, EXERCISES as TWO_TASKS
from core.primer_appendix_more import GUIDES as LONGER, EXERCISES as LONGER_TASKS
from core.primer_appendix_studies import GUIDES as STUDIES, EXERCISES as STUDY_TASKS

GUIDES = {**FOUNDATIONS, **TWO_MOVERS, **LONGER, **STUDIES}
EXERCISES = [*FOUNDATION_TASKS, *TWO_TASKS, *LONGER_TASKS, *STUDY_TASKS]
