"""Generation-side checks based on token overlap. They are cheap, transparent
baselines; swap in an NLI model or an LLM judge for production use."""
from .text import tokens, sentences


def _overlap(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a) if a else 0.0


def context_relevance(question, contexts):
    """Per-context share of question terms it contains."""
    q = tokens(question)
    return [_overlap(q, tokens(c)) for c in contexts]


def groundedness(answer, contexts, threshold=0.6):
    """Share of answer sentences whose terms are mostly found in the contexts.

    Returns (score, unsupported_sentences)."""
    ctx = set(tokens(" ".join(contexts)))
    sents = sentences(answer)
    unsupported = [s for s in sents if _overlap(tokens(s), ctx) < threshold]
    score = 1 - len(unsupported) / len(sents) if sents else 0.0
    return score, unsupported


def answer_correctness(answer, reference):
    """Token-level F1 against a reference answer (SQuAD style)."""
    a, r = tokens(answer), tokens(reference)
    if not a or not r:
        return float(a == r)
    common = sum(min(a.count(t), r.count(t)) for t in set(a))
    if common == 0:
        return 0.0
    p, rc = common / len(a), common / len(r)
    return 2 * p * rc / (p + rc)
