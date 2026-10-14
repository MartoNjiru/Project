import unittest

from redteam import build_prompts, is_refusal, leaks_secret, run_suite
from redteam.mock_models import SECRET, naive_model, safe_model


class TestDetectors(unittest.TestCase):
    def test_refusal(self):
        self.assertTrue(is_refusal("Sorry, but I can't help with that."))
        self.assertFalse(is_refusal("Sure, here you go."))

    def test_leak(self):
        self.assertTrue(leaks_secret("value is token-1234", ["TOKEN-1234"]))


class TestRunner(unittest.TestCase):
    def test_build(self):
        prompts = build_prompts(["x"], ["role_play"])
        self.assertEqual(len(prompts), 2)

    def test_safe_model_passes(self):
        rep = run_suite(safe_model, ["x"], secrets=[SECRET])
        self.assertEqual(rep.attack_success_rate, 0.0)

    def test_naive_model_fails_some(self):
        rep = run_suite(naive_model, ["x"], secrets=[SECRET])
        cats = rep.by_category()
        self.assertEqual(cats["direct_request"]["failures"], 0)
        self.assertGreater(cats["role_play"]["failures"], 0)
        self.assertEqual(cats["prompt_injection"]["failures"], 2)
        self.assertIn("| Category |", rep.to_markdown())


if __name__ == "__main__":
    unittest.main()
