"""Score each claim against a trusted reference context.

Two signals are combined:
1. Lexical support  - share of the claim's content words found in the best-matching
   reference sentence.
2. Fact consistency - numbers, years and capitalised entities in the claim must
   appear in the reference. A number/entity that never appears is a strong
   hallucination signal (fabricated dates, figures, names).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict

from .claims import split_claims, is_hedged

STOPWORDS = set("""a an the and or but if of to in on at by for with from as is are was were be been
being it its this that these those there their they he she his her we our you your i not no
has have had do does did so than then which who whom what when where why how also into over
about after before such can will would should may""".split())

_NUM = re.compile(r"\b\d+(?:[.,]\d+)?%?\b")
_ENTITY = re.compile(r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b")


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS and len(w) > 1}


def _entities(text: str) -> set[str]:
    ents = set()
    for m in _ENTITY.finditer(text):
        # skip a capitalised first word of the sentence when it is a stopword
        word = m.group(0)
        if word.lower() in STOPWORDS:
            continue
        ents.add(word.lower())
    return ents


@dataclass
class ClaimResult:
    claim: str
    support: float
    missing_numbers: list[str] = field(default_factory=list)
    missing_entities: list[str] = field(default_factory=list)
    hedged: bool = False
    evidence: str = ""

    @property
    def label(self) -> str:
        if self.missing_numbers:
            return "contradicted_or_fabricated"
        if self.support >= 0.6 and not self.missing_entities:
            return "supported"
        if self.support >= 0.35:
            return "partially_supported"
        return "unsupported"


@dataclass
class AnswerReport:
    claims: list[ClaimResult]

    @property
    def hallucination_rate(self) -> float:
        if not self.claims:
            return 0.0
        bad = sum(c.label in ("unsupported", "contradicted_or_fabricated") for c in self.claims)
        return round(bad / len(self.claims), 3)

    @property
    def faithfulness(self) -> float:
        if not self.claims:
            return 1.0
        return round(sum(c.support for c in self.claims) / len(self.claims), 3)

    def to_dict(self) -> dict:
        return {
            "faithfulness": self.faithfulness,
            "hallucination_rate": self.hallucination_rate,
            "claims": [dict(asdict(c), label=c.label) for c in self.claims],
        }


def check_answer(answer: str, reference: str) -> AnswerReport:
    ref_sents = split_claims(reference) or [reference]
    ref_tokens_all = _tokens(reference)
    ref_numbers = set(_NUM.findall(reference))
    ref_entities = _entities(reference)

    results = []
    for claim in split_claims(answer):
        ctoks = _tokens(claim)
        best, evidence = 0.0, ""
        for sent in ref_sents:
            stoks = _tokens(sent)
            if not ctoks:
                break
            score = len(ctoks & stoks) / len(ctoks)
            if score > best:
                best, evidence = score, sent
        # small credit for words supported anywhere in the reference
        if ctoks:
            global_cov = len(ctoks & ref_tokens_all) / len(ctoks)
            best = max(best, 0.8 * global_cov)
        results.append(ClaimResult(
            claim=claim,
            support=round(best, 3),
            missing_numbers=sorted(set(_NUM.findall(claim)) - ref_numbers),
            missing_entities=sorted(_entities(claim) - ref_entities - STOPWORDS),
            hedged=is_hedged(claim),
            evidence=evidence,
        ))
    return AnswerReport(results)
