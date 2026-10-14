# Prompt Regression Tester

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Unit tests for prompts. Write assertions about what a good answer looks like, run the suite against a model, then compare two runs to catch regressions before you ship a new prompt or model version.

## Features
| Module | What it does |
|---|---|
| `assertions.py` | `contains`, `not_contains`, `regex`, `max_words`, `min_words`, `is_json`, `starts_with`, `one_of` |
| `runner.py` | Run a suite through any `prompt -> str` callable; diff two runs into regressions, fixes and still-failing |
| `models.py` | Replay recorded outputs so suites run offline in CI |

## Quick start
```bash
python -m promptreg examples/suite.json --baseline examples/baseline_outputs.json --candidate examples/candidate_outputs.json
```
```
Baseline pass rate: 100%
Candidate pass rate: 50%
  regressions: ['capital', 'json']
  fixes: none
  still_failing: none
```

## Data format
A suite is `{"template": "...{input}...", "cases": [{"id", "input", "assert": [{"contains": "Nairobi"}]}]}`.

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- The CLI exits with code 1 when there are regressions, so it can block a merge in CI.
- To test a live model, pass any function that takes a prompt and returns text to `run_suite`.

## License
MIT, by Martin Njiru.
