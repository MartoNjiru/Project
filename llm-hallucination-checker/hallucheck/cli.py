"""Usage: python -m hallucheck.cli examples/qa.jsonl

Each JSONL line needs: {"id": ..., "reference": "...", "answer": "..."}
"""
import json
import sys

from .checker import check_answer


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    rows = [json.loads(l) for l in open(argv[0], encoding="utf-8") if l.strip()]
    total = 0.0
    print(f"{'id':<8}{'faithful':>10}{'halluc.':>10}  flagged claims")
    for row in rows:
        rep = check_answer(row["answer"], row["reference"])
        total += rep.hallucination_rate
        flagged = [c.claim for c in rep.claims if c.label != "supported"]
        print(f"{row['id']:<8}{rep.faithfulness:>10.2f}{rep.hallucination_rate:>10.2f}  {flagged[:2]}")
    print(f"\nMean hallucination rate: {total / max(len(rows), 1):.2f} over {len(rows)} answers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
