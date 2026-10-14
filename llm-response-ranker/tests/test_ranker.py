import unittest

from ranker import EloRanker, bradley_terry, cohen_kappa, percent_agreement, score_response


class TestRubric(unittest.TestCase):
    def test_refusal_penalised(self):
        good = score_response("Explain recursion in Python.", "Recursion in Python is when a function calls itself " * 8)
        bad = score_response("Explain recursion in Python.", "I'm unable to help with that.")
        self.assertGreater(good["total"], bad["total"])
        self.assertEqual(bad["no_unneeded_refusal"], 0.0)

    def test_count_constraint(self):
        r = score_response("Give 3 tips.", "1. a\n2. b\n3. c")
        self.assertEqual(r["instruction_following"], 1.0)


class TestRanking(unittest.TestCase):
    comps = [("A", "B", 1), ("A", "C", 1), ("B", "C", 1), ("A", "B", 1), ("C", "B", 0)]

    def test_elo_order(self):
        board = EloRanker().fit(self.comps).leaderboard()
        self.assertEqual([m for m, _ in board], ["A", "B", "C"])

    def test_bt_order(self):
        self.assertEqual(list(bradley_terry(self.comps)), ["A", "B", "C"])


class TestAgreement(unittest.TestCase):
    def test_perfect(self):
        self.assertEqual(cohen_kappa(list("abab"), list("abab")), 1.0)

    def test_percent(self):
        self.assertEqual(percent_agreement(list("aab"), list("abb")), 2 / 3)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            percent_agreement([1], [1, 2])


if __name__ == "__main__":
    unittest.main()
