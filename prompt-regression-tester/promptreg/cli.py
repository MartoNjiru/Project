import argparse
import json
import sys

from .models import recorded
from .runner import run_suite, diff_runs, save


def main(argv=None):
    p = argparse.ArgumentParser(description="Run a prompt test suite and compare model versions")
    p.add_argument("suite", help="suite JSON: {\"template\": ..., \"cases\": [...]}")
    p.add_argument("--baseline", required=True, help="recorded outputs JSON for the current model")
    p.add_argument("--candidate", help="recorded outputs JSON for the new model/prompt")
    p.add_argument("--out", help="save reports to this prefix")
    a = p.parse_args(argv)
    suite = json.load(open(a.suite, encoding="utf-8"))
    base = run_suite(suite["cases"], recorded(a.baseline), suite.get("template"))
    print(f"Baseline pass rate: {base['pass_rate']:.0%}")
    for cid, r in base["results"].items():
        if not r["passed"]:
            print(f"  FAIL {cid}: {', '.join(r['failures'])}")
    if not a.candidate:
        return
    cand = run_suite(suite["cases"], recorded(a.candidate), suite.get("template"))
    print(f"Candidate pass rate: {cand['pass_rate']:.0%}")
    d = diff_runs(base, cand)
    for k, v in d.items():
        print(f"  {k}: {v or 'none'}")
    if a.out:
        save(base, a.out + "_baseline.json")
        save(cand, a.out + "_candidate.json")
    if d["regressions"]:
        sys.exit(1)
