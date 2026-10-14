"""Split an LLM answer into atomic, checkable claims."""
import re

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
_HEDGES = ("i think", "maybe", "perhaps", "it is possible", "might", "could be")


def split_claims(text: str) -> list[str]:
    """Return sentence-level claims, dropping empty lines and pure hedges/questions."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    claims = []
    for sent in _SENT_SPLIT.split(text):
        sent = sent.strip(" -*•")
        if not sent or sent.endswith("?"):
            continue
        claims.append(sent)
    return claims


def is_hedged(claim: str) -> bool:
    low = claim.lower()
    return any(h in low for h in _HEDGES)
