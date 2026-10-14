"""Usage: python -m ranker examples/preferences.jsonl

Each line: {"prompt": ..., "model_a": ..., "model_b": ..., "response_a": ..., "response_b": ...,
            "annotator_1": "a"|"b"|"tie", "annotator_2": "a"|"b"|"tie"}
"""
import json
import sys

from . import EloRanker, bradley_terry, cohen_kappa, score_response

OUT = {"a": 1.0, "b": 0.0, "tie": 0.5}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    comps, ann1, ann2, rubric_hits = [], [], [], 0
    for r in rows:
        comps.append((r["model_a"], r["model_b"], OUT[r["annotator_1"]]))
        ann1.append(r["annotator_1"]); ann2.append(r["annotator_2"])
        sa = score_response(r["prompt"], r["response_a"])["total"]
        sb = score_response(r["prompt"], r["response_b"])["total"]
        rubric_pick = "a" if sa > sb else "b" if sb > sa else "tie"
        rubric_hits += rubric_pick == r["annotator_1"]
    print("Elo leaderboard:", EloRanker().fit(comps).leaderboard())
    print("Bradley-Terry:  ", bradley_terry(comps))
    print(f"Annotator Cohen's kappa: {cohen_kappa(ann1, ann2):.2f}")
    print(f"Rubric baseline agrees with annotator 1 on {rubric_hits}/{len(rows)} pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
