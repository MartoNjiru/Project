# LLM Response Ranker

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

A toolkit for RLHF-style preference evaluation: score single responses against a rubric, turn pairwise human judgements into model leaderboards, and measure how consistent annotators are.

## Features
| Module | What it does |
|---|---|
| `rubric.py` | Weighted rubric: instruction following (such as "give 3 tips"), completeness, concision, unneeded refusals and formatting |
| `elo.py` | Online Elo ratings, the approach chatbot arenas use |
| `bradley_terry.py` | Order-independent Bradley-Terry strengths (MM algorithm) for fixed batches of labels |
| `agreement.py` | Percent agreement and Cohen's kappa between annotators |

## Quick start
```bash
python -m ranker examples/preferences.jsonl
```
```
Elo leaderboard: [('gpt-x', 1025.7), ('llama-y', 1018.7), ('mistral-z', 955.6)]
Bradley-Terry:   {'llama-y': 1.4995, 'gpt-x': 1.4955, 'mistral-z': 0.005}
Annotator Cohen's kappa: 0.58
Rubric baseline agrees with annotator 1 on 5/5 pairs
```

## Data format
One JSON object per line: `prompt`, `model_a`, `model_b`, `response_a`, `response_b`, `annotator_1`, `annotator_2` (each `"a"`, `"b"` or `"tie"`).

## Notes
- Elo depends on the order of comparisons. Bradley-Terry doesn't, so use it to report results on a fixed batch.
- A kappa under about 0.6 usually means the guidelines need clarifying before the labels can be trusted.
- The rubric is heuristic and works best as a sanity check on human labels or a cheap pre-filter.

## Run the tests
```bash
python -m unittest discover -s tests -v
```

Pure Python 3.10+, no third-party dependencies.

## License
MIT
