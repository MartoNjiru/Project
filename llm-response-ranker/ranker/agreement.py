"""Inter-annotator agreement metrics for preference labels."""
from collections import Counter


def percent_agreement(a: list, b: list) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("label lists must be the same non-zero length")
    return sum(x == y for x, y in zip(a, b)) / len(a)


def cohen_kappa(a: list, b: list) -> float:
    po = percent_agreement(a, b)
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    return 1.0 if pe == 1 else round((po - pe) / (1 - pe), 4)
