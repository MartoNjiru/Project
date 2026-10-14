"""ranker: tools for pairwise preference evaluation of LLM responses (RLHF-style)."""
from .rubric import Rubric, score_response
from .elo import EloRanker
from .bradley_terry import bradley_terry
from .agreement import cohen_kappa, percent_agreement

__all__ = ["Rubric", "score_response", "EloRanker", "bradley_terry", "cohen_kappa", "percent_agreement"]
__version__ = "0.1.0"
