import unittest
from promptreg import run_assertion, run_suite, diff_runs

SUITE = [{"id": "a", "input": "q1", "assert": [{"contains": "yes"}]},
         {"id": "b", "input": "q2", "assert": [{"max_words": 2}]}]


class TestAssertions(unittest.TestCase):
    def test_kinds(self):
        self.assertTrue(run_assertion("Nairobi", {"contains": "nairobi"})[0])
        self.assertTrue(run_assertion('{"a": 1}', {"is_json": True})[0])
        self.assertFalse(run_assertion("one two three", {"max_words": 2})[0])
        self.assertTrue(run_assertion("ID 42", {"regex": r"\d+"})[0])
        with self.assertRaises(ValueError):
            run_assertion("x", {"nope": 1})


class TestRunner(unittest.TestCase):
    def test_suite_and_diff(self):
        old = run_suite(SUITE, {"q1": "yes", "q2": "too many words here"}.get)
        new = run_suite(SUITE, {"q1": "no", "q2": "short"}.get)
        self.assertEqual(old["pass_rate"], 0.5)
        d = diff_runs(old, new)
        self.assertEqual(d["regressions"], ["a"])
        self.assertEqual(d["fixes"], ["b"])

    def test_template(self):
        seen = []
        run_suite([{"id": "x", "input": "hi"}], lambda p: seen.append(p) or "", "Q: {input}")
        self.assertEqual(seen, ["Q: hi"])


if __name__ == "__main__":
    unittest.main()
