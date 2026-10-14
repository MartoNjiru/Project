import unittest
from outguard import extract_json, validate, find_pii, redact, check_rules

SCHEMA = {"type": "object", "required": ["a"], "properties": {"a": {"type": "integer", "minimum": 0},
          "tags": {"type": "array", "items": {"type": "string"}}}}


class TestJson(unittest.TestCase):
    def test_extract_from_fence_and_prose(self):
        self.assertEqual(extract_json("ok ```json\n{\"a\": 1}\n``` done"), {"a": 1})
        self.assertEqual(extract_json("Answer: [1, 2] thanks"), [1, 2])
        with self.assertRaises(ValueError):
            extract_json("no json here")

    def test_validate(self):
        self.assertEqual(validate({"a": 2, "tags": ["x"]}, SCHEMA), [])
        errs = validate({"a": -1, "tags": ["x", 3]}, SCHEMA)
        self.assertEqual(len(errs), 2)
        self.assertIn("$.a: missing", validate({}, SCHEMA))
        self.assertTrue(validate({"a": True}, SCHEMA))  # bool is not an integer


class TestPII(unittest.TestCase):
    def test_kenyan_phone_and_email(self):
        kinds = {k for k, _ in find_pii("Call +254712345678 or mail a.b@mail.co.ke")}
        self.assertEqual(kinds, {"ke_phone", "email"})

    def test_card_needs_luhn(self):
        self.assertIn("card", {k for k, _ in find_pii("card 4111 1111 1111 1111")})
        self.assertNotIn("card", {k for k, _ in find_pii("order 1234 5678 9012 3456")})

    def test_redact(self):
        self.assertEqual(redact("Mail me at x@y.com"), "Mail me at [EMAIL]")


class TestRules(unittest.TestCase):
    def test_rules(self):
        self.assertEqual(check_rules("Three short words", max_words=5), [])
        probs = check_rules("I can't help with that, as an AI", must_include=["Nairobi"])
        self.assertEqual(len(probs), 2)


if __name__ == "__main__":
    unittest.main()
