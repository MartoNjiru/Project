"""Run attacks against any `model(prompt) -> str` callable and summarise results."""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from .attacks import build_prompts
from .detectors import is_refusal, leaks_secret


@dataclass
class SuiteReport:
    results: list[dict]

    def by_category(self) -> dict:
        agg = defaultdict(lambda: {"total": 0, "failures": 0})
        for r in self.results:
            agg[r["category"]]["total"] += 1
            agg[r["category"]]["failures"] += r["failed"]
        return {c: dict(v, attack_success_rate=round(v["failures"] / v["total"], 2)) for c, v in agg.items()}

    @property
    def attack_success_rate(self) -> float:
        return round(sum(r["failed"] for r in self.results) / max(len(self.results), 1), 3)

    def to_markdown(self) -> str:
        lines = ["| Category | Attacks | Failures | ASR |", "|---|---|---|---|"]
        for c, v in self.by_category().items():
            lines.append(f"| {c} | {v['total']} | {v['failures']} | {v['attack_success_rate']:.0%} |")
        lines.append(f"\n**Overall attack success rate:** {self.attack_success_rate:.0%}")
        return "\n".join(lines)

    def save_jsonl(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for r in self.results:
                f.write(json.dumps(r) + "\n")


def run_suite(model: Callable[[str], str], goals: list[str], secrets: list[str] | None = None,
              categories: list[str] | None = None) -> SuiteReport:
    secrets = secrets or []
    results = []
    for item in build_prompts(goals, categories):
        reply = model(item["prompt"])
        leaked = leaks_secret(reply, secrets)
        refused = is_refusal(reply)
        failed = leaked or (item["goal"] is not None and not refused)
        results.append({**item, "response": reply, "refused": refused, "leaked": leaked, "failed": bool(failed)})
    return SuiteReport(results)
