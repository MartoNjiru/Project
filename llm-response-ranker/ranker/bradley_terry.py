"""Bradley-Terry strengths via the classic MM (minorise-maximise) algorithm.

Order-independent, unlike Elo, so it is the better choice for a fixed batch of
preference labels.
"""
from collections import defaultdict


def bradley_terry(comparisons, iters: int = 200, tol: float = 1e-8) -> dict:
    wins = defaultdict(float)
    pair_counts = defaultdict(float)
    items = set()
    for a, b, outcome in comparisons:
        items.update((a, b))
        wins[a] += outcome
        wins[b] += 1 - outcome
        pair_counts[frozenset((a, b))] += 1
    p = {i: 1.0 for i in items}
    for _ in range(iters):
        new = {}
        for i in items:
            denom = sum(n / (p[i] + p[j]) for pair, n in pair_counts.items() if i in pair
                        for j in pair if j != i)
            new[i] = (wins[i] + 0.01) / denom if denom else p[i]
        s = sum(new.values())
        new = {i: v * len(items) / s for i, v in new.items()}
        if max(abs(new[i] - p[i]) for i in items) < tol:
            p = new
            break
        p = new
    return dict(sorted(((i, round(v, 4)) for i, v in p.items()), key=lambda x: -x[1]))
