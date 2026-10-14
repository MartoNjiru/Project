"""Elo ratings from pairwise comparisons (as used in chatbot arenas)."""
from collections import defaultdict


class EloRanker:
    def __init__(self, k: float = 32, base: float = 1000):
        self.k = k
        self.ratings = defaultdict(lambda: base)

    def expected(self, a: str, b: str) -> float:
        return 1 / (1 + 10 ** ((self.ratings[b] - self.ratings[a]) / 400))

    def update(self, a: str, b: str, outcome: float) -> None:
        """outcome: 1 if a wins, 0 if b wins, 0.5 for a tie."""
        ea = self.expected(a, b)
        self.ratings[a] += self.k * (outcome - ea)
        self.ratings[b] += self.k * ((1 - outcome) - (1 - ea))

    def fit(self, comparisons):
        for a, b, outcome in comparisons:
            self.update(a, b, outcome)
        return self

    def leaderboard(self):
        return sorted(((m, round(r, 1)) for m, r in self.ratings.items()), key=lambda x: -x[1])
