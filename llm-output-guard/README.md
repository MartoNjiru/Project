# LLM Output Guard

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Guardrails for LLM output before it reaches users or downstream code: pull JSON out of chatty responses, validate it against a schema, catch personal data and enforce format rules.

## Features
| Module | What it does |
|---|---|
| `jsoncheck.py` | Extract JSON from prose or ```json fences; validate type, required keys, enum, min/max, nested arrays |
| `pii.py` | Detect and redact emails, Kenyan (+254 / 07xx / 01xx) and international phone numbers, ID numbers, and card numbers (Luhn-checked to cut false positives) |
| `rules.py` | Word limits, required and banned terms, refusal detection |

## Quick start
```bash
python -m outguard examples/outputs.jsonl --schema examples/schema.json
```
```
#1 PASS
#2 FAIL
   - $.sentiment: 'angry' not in ['positive', 'negative', 'neutral']
   - $.score: above 1
#3 FAIL
   - PII email: jane@example.com
   - PII ke_phone: 0712345678

1/3 outputs passed
```

## Data format
`outputs.jsonl` holds one `{"output": ...}` per line; the schema uses a small JSON Schema subset (`type`, `properties`, `required`, `items`, `enum`, `minLength`, `minimum`, `maximum`).

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- `True` is rejected where an integer is expected, a classic Python pitfall.
- PII patterns are a baseline, not a compliance guarantee.

## License
MIT, by Martin Njiru.
