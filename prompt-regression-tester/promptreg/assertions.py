import json
import re


def _json_ok(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


CHECKS = {
    "contains": lambda out, v: v.lower() in out.lower(),
    "not_contains": lambda out, v: v.lower() not in out.lower(),
    "regex": lambda out, v: re.search(v, out) is not None,
    "max_words": lambda out, v: len(out.split()) <= v,
    "min_words": lambda out, v: len(out.split()) >= v,
    "is_json": lambda out, v: _json_ok(out) == bool(v),
    "starts_with": lambda out, v: out.strip().lower().startswith(v.lower()),
    "one_of": lambda out, v: out.strip().lower() in [x.lower() for x in v],
}


def run_assertion(output, assertion):
    """assertion is a one-key dict such as {"contains": "Nairobi"}. Returns (ok, message)."""
    (kind, value), = assertion.items()
    if kind not in CHECKS:
        raise ValueError(f"unknown assertion: {kind}")
    ok = CHECKS[kind](output, value)
    return ok, f"{kind}={value!r}"
