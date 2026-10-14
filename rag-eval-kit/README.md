# RAG Eval Kit

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Evaluate both halves of a retrieval-augmented generation pipeline: did the retriever find the right documents, and did the answer stay grounded in them?

## Features
| Module | What it does |
|---|---|
| `retrieval.py` | Precision@k, Recall@k, Hit rate, MRR and nDCG@k (binary or graded relevance) |
| `generation.py` | Context relevance, groundedness (flags answer sentences the context doesn't support) and SQuAD-style answer F1 |

## Quick start
```bash
python -m rageval examples/run.jsonl -k 3
```
```
[unsupported] 'What is the capital of Kenya?': It has a population of 40 million people.

3 questions, k=3
       P@3: 0.444
       R@3: 1.000
     Hit@3: 1.000
       MRR: 0.667
    nDCG@3: 0.775
  Grounded: 0.833
  AnswerF1: 0.556
```

## Data format
One JSON object per line: `question`, `retrieved` (ranked doc ids), `relevant` (doc ids), `contexts` (retrieved text), `answer`, `reference`.

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- Groundedness uses token overlap: transparent and fast, but swap in an NLI model or LLM judge for production.
- The example catches an invented claim ("population of 40 million") that isn't in the retrieved context.

## License
MIT, by Martin Njiru.
