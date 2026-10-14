# LLM Hallucination Checker

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Splits an LLM answer into sentence-level claims and scores each one against a trusted reference passage, flagging hallucinations such as invented numbers, dates and named entities.

## Why
Fact-checking model outputs is a core part of RLHF and evaluation work. This tool gives a fast, transparent first pass before a human reviewer looks at the flagged claims.

## How it works
1. **Claim splitting** breaks the answer into atomic sentences and skips questions and filler.
2. **Lexical support** measures how much of each claim's content is backed by the best-matching reference sentence.
3. **Fact consistency** checks that every number and capitalised entity in a claim appears in the reference. A missing figure is labelled `contradicted_or_fabricated`.

Each claim gets one of four labels: `supported`, `partially_supported`, `unsupported` or `contradicted_or_fabricated`. Each answer also gets a **faithfulness** score and a **hallucination rate**.

## Quick start
```bash
python -m hallucheck examples/qa.jsonl
```
```
id        faithful   halluc.  flagged claims
q1            0.92      0.00  []
q2            0.56      1.00  ['Lake Nakuru National Park covers about 400 square kilometres.', ...]
q3            0.27      0.50  ['...', 'It also removed the GIL by default.']
```

```python
from hallucheck import check_answer
report = check_answer(answer="The tower was completed in 1925.",
                      reference="The Eiffel Tower was completed in 1889.")
print(report.to_dict())
```

## Limitations
This is a lexical baseline. It cannot catch paraphrased contradictions ("not founded in 1939") or reasoning errors. A natural next step is an NLI model or an LLM-as-judge stage for the claims it marks as `partially_supported`.

## Run the tests
```bash
python -m unittest discover -s tests -v
```

Pure Python 3.10+, no third-party dependencies.

## License
MIT
