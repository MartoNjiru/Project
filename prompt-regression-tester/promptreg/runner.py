import json


def run_suite(suite, model, template=None):
    """suite: list of {"id", "input", "assert": [...]}.

    `template` is an optional prompt template with an {input} slot.
    Returns {"results": {id: {"passed", "failures", "output"}}, "pass_rate"}."""
    from .assertions import run_assertion
    results = {}
    for case in suite:
        prompt = template.format(input=case["input"]) if template else case["input"]
        out = model(prompt)
        failures = [msg for ok, msg in (run_assertion(out, a) for a in case.get("assert", [])) if not ok]
        results[case["id"]] = {"passed": not failures, "failures": failures, "output": out}
    passed = sum(r["passed"] for r in results.values())
    return {"results": results, "pass_rate": passed / len(results) if results else 0.0}


def diff_runs(old, new):
    """Compare two run_suite reports. Returns dict of regressions/fixes/still_failing."""
    o, n = old["results"], new["results"]
    common = o.keys() & n.keys()
    return {
        "regressions": sorted(k for k in common if o[k]["passed"] and not n[k]["passed"]),
        "fixes": sorted(k for k in common if not o[k]["passed"] and n[k]["passed"]),
        "still_failing": sorted(k for k in common if not o[k]["passed"] and not n[k]["passed"]),
    }


def save(report, path):
    json.dump(report, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
