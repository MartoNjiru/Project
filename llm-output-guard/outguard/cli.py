import argparse
import json

from .jsoncheck import extract_json, validate
from .pii import find_pii


def main(argv=None):
    p = argparse.ArgumentParser(description="Check LLM outputs against a JSON schema and for PII")
    p.add_argument("outputs", help="JSONL with an 'output' field per line")
    p.add_argument("--schema", help="JSON schema file")
    a = p.parse_args(argv)
    schema = json.load(open(a.schema)) if a.schema else None
    passed = total = 0
    for n, line in enumerate(open(a.outputs, encoding="utf-8"), 1):
        if not line.strip():
            continue
        total += 1
        text = json.loads(line)["output"]
        issues = []
        if schema:
            try:
                issues += validate(extract_json(text), schema)
            except ValueError as e:
                issues.append(str(e))
        issues += [f"PII {k}: {v}" for k, v in find_pii(text)]
        passed += not issues
        print(f"#{n} {'PASS' if not issues else 'FAIL'}" + "".join(f"\n   - {i}" for i in issues))
    print(f"\n{passed}/{total} outputs passed")
