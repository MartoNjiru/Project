"""Lightweight, dependency-free RAG evaluation."""
from .retrieval import precision_at_k, recall_at_k, hit_rate, mrr, ndcg_at_k
from .generation import context_relevance, groundedness, answer_correctness
__all__ = ["precision_at_k", "recall_at_k", "hit_rate", "mrr", "ndcg_at_k",
           "context_relevance", "groundedness", "answer_correctness"]
