import unittest

from hallucheck import check_answer, split_claims

REF = "The Eiffel Tower is in Paris, France. It was completed in 1889 and is 330 metres tall."


class TestClaims(unittest.TestCase):
    def test_split(self):
        self.assertEqual(len(split_claims("One fact. Two facts! Is this a question?")), 2)

    def test_empty(self):
        self.assertEqual(split_claims("   "), [])


class TestChecker(unittest.TestCase):
    def test_faithful_answer(self):
        rep = check_answer("The Eiffel Tower is in Paris. It was completed in 1889.", REF)
        self.assertEqual(rep.hallucination_rate, 0.0)
        self.assertTrue(all(c.label == "supported" for c in rep.claims))

    def test_fabricated_number(self):
        rep = check_answer("The Eiffel Tower was completed in 1925.", REF)
        self.assertEqual(rep.claims[0].label, "contradicted_or_fabricated")
        self.assertIn("1925", rep.claims[0].missing_numbers)

    def test_unsupported_entity(self):
        rep = check_answer("The Eiffel Tower was designed by Leonardo da Vinci in Rome.", REF)
        self.assertNotEqual(rep.claims[0].label, "supported")

    def test_report_dict(self):
        d = check_answer("The tower is in Paris.", REF).to_dict()
        self.assertIn("faithfulness", d)
        self.assertIn("label", d["claims"][0])


if __name__ == "__main__":
    unittest.main()
