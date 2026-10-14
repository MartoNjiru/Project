"""Ranking metrics. `retrieved` is an ordered list of doc ids; `relevant` a set
(or a dict id -> graded relevance for nDCG)."""
import math


def precision_at_k(retrieved, relevant, k):
    top = retrieved[:k]
    return sum(d in relevant for d in top) / k if k else 0.0


def recall_at_k(retrieved, relevant, k):
    if not relevant:
        return 0.0
    return len(set(retrieved[:k]) & set(relevant)) / len(relevant)


def hit_rate(retrieved, relevant, k):
    return float(any(d in relevant for d in retrieved[:k]))


def mrr(retrieved, relevant):
    for rank, d in enumerate(retrieved, 1):
        if d in relevant:
            return 1 / rank
    return 0.0


def ndcg_at_k(retrieved, relevance, k):
    if not isinstance(relevance, dict):
        relevance = {d: 1 for d in relevance}
    dcg = sum(relevance.get(d, 0) / math.log2(i + 2) for i, d in enumerate(retrieved[:k]))
    ideal = sorted(relevance.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0
