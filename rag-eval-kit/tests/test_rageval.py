import unittest
from rageval import (precision_at_k, recall_at_k, hit_rate, mrr, ndcg_at_k,
                     context_relevance, groundedness, answer_correctness)


class TestRetrieval(unittest.TestCase):
    def test_precision_recall(self):
        self.assertAlmostEqual(precision_at_k(["a", "b", "c"], {"a", "c"}, 3), 2 / 3)
        self.assertAlmostEqual(recall_at_k(["a", "b"], {"a", "c"}, 2), 0.5)
        self.assertEqual(hit_rate(["x", "y"], {"y"}, 1), 0.0)

    def test_mrr(self):
        self.assertEqual(mrr(["x", "y", "z"], {"z"}), 1 / 3)
        self.assertEqual(mrr(["x"], {"q"}), 0.0)

    def test_ndcg(self):
        self.assertAlmostEqual(ndcg_at_k(["a", "b"], {"a": 3, "b": 1}, 2), 1.0)
        self.assertLess(ndcg_at_k(["b", "a"], {"a": 3, "b": 1}, 2), 1.0)


class TestGeneration(unittest.TestCase):
    def test_groundedness_flags_invention(self):
        ctx = ["Nairobi is the capital of Kenya."]
        score, bad = groundedness("Nairobi is the capital of Kenya. It hosts the 2030 Olympics.", ctx)
        self.assertEqual(score, 0.5)
        self.assertEqual(len(bad), 1)

    def test_context_relevance(self):
        rel = context_relevance("capital of Kenya", ["Kenya capital Nairobi", "football scores"])
        self.assertGreater(rel[0], rel[1])

    def test_answer_f1(self):
        self.assertEqual(answer_correctness("Nairobi", "Nairobi"), 1.0)
        self.assertEqual(answer_correctness("Mombasa", "Nairobi"), 0.0)


if __name__ == "__main__":
    unittest.main()
