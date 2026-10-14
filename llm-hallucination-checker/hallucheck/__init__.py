"""hallucheck: lightweight, dependency-free hallucination checks for LLM answers."""
from .claims import split_claims
from .checker import check_answer, ClaimResult, AnswerReport

__all__ = ["split_claims", "check_answer", "ClaimResult", "AnswerReport"]
__version__ = "0.1.0"
