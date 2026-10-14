"""Rubric-based scoring of a single response.

Heuristic, transparent checks that mirror common annotation guidelines
(instruction following, completeness, concision, safety, formatting). They are
not a replacement for a human or LLM judge, but they make a fast baseline and a
sanity check for annotator scores.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REFUSAL = re.compile(r"\b(i can(?:no|')t|i am unable|i'm unable|as an ai)\b", re.I)
FILLER = re.compile(r"\b(great question|certainly!|i hope this helps|feel free to)\b", re.I)


@dataclass
class Rubric:
    weights: dict = field(default_factory=lambda: {
        "instruction_following": 0.35,
        "completeness": 0.25,
        "concision": 0.15,
        "no_unneeded_refusal": 0.15,
        "formatting": 0.10,
    })
    ideal_words: tuple = (40, 250)


def _keywords(prompt: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]{4,}", prompt.lower())
    stop = {"what", "which", "please", "explain", "write", "give", "about", "with", "that", "this", "your", "from", "list", "describe"}
    return {w for w in words if w not in stop}


def score_response(prompt: str, response: str, rubric: Rubric | None = None) -> dict:
    rubric = rubric or Rubric()
    words = response.split()
    n = len(words)
    kws = _keywords(prompt)
    covered = sum(1 for k in kws if k in response.lower())

    scores = {}
    scores["completeness"] = covered / len(kws) if kws else 1.0

    # Instruction following: numeric constraints like "3 tips" / "in 2 sentences"
    m = re.search(r"\b(\d+)\s+(tips|points|bullets|reasons|steps|examples|sentences)\b", prompt.lower())
    if m:
        want = int(m.group(1))
        if m.group(2) == "sentences":
            got = len([s for s in re.split(r"[.!?]+", response) if s.strip()])
        else:
            got = len(re.findall(r"^\s*(?:[-*•]|\d+[.)])\s+", response, re.M))
        scores["instruction_following"] = max(0.0, 1 - abs(got - want) / want)
    else:
        scores["instruction_following"] = scores["completeness"]

    lo, hi = rubric.ideal_words
    if n < lo:
        conc = n / lo
    elif n > hi:
        conc = max(0.0, 1 - (n - hi) / hi)
    else:
        conc = 1.0
    conc -= 0.1 * len(FILLER.findall(response))
    scores["concision"] = max(0.0, min(1.0, conc))

    scores["no_unneeded_refusal"] = 0.0 if REFUSAL.search(response) else 1.0
    scores["formatting"] = 0.5 if re.search(r"(.)\1{5,}", response) else 1.0

    total = sum(rubric.weights[k] * scores[k] for k in rubric.weights)
    return {"total": round(total, 3), **{k: round(v, 3) for k, v in scores.items()}}
