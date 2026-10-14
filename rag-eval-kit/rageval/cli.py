import argparse
import json
from statistics import mean

from .retrieval import precision_at_k, recall_at_k, hit_rate, mrr, ndcg_at_k
from .generation import groundedness, answer_correctness


def main(argv=None):
    p = argparse.ArgumentParser(description="Evaluate a RAG run")
    p.add_argument("path", help="JSONL with question, retrieved, relevant, contexts, answer, reference")
    p.add_argument("-k", type=int, default=3)
    a = p.parse_args(argv)
    rows = [json.loads(l) for l in open(a.path, encoding="utf-8") if l.strip()]
    m = {k: [] for k in ["P@k", "R@k", "Hit@k", "MRR", "nDCG@k", "Grounded", "AnswerF1"]}
    for r in rows:
        rel = set(r["relevant"])
        m["P@k"].append(precision_at_k(r["retrieved"], rel, a.k))
        m["R@k"].append(recall_at_k(r["retrieved"], rel, a.k))
        m["Hit@k"].append(hit_rate(r["retrieved"], rel, a.k))
        m["MRR"].append(mrr(r["retrieved"], rel))
        m["nDCG@k"].append(ndcg_at_k(r["retrieved"], rel, a.k))
        g, bad = groundedness(r["answer"], r["contexts"])
        m["Grounded"].append(g)
        m["AnswerF1"].append(answer_correctness(r["answer"], r["reference"]))
        for s in bad:
            print(f"[unsupported] {r['question']!r}: {s}")
    print(f"\n{len(rows)} questions, k={a.k}")
    for k, v in m.items():
        print(f"{k.replace('k', str(a.k)) if '@' in k else k:>10}: {mean(v):.3f}")
