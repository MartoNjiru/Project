# LLM Evaluation Toolkit

![tests](https://github.com/MartoNjiru/llm-evaluation-toolkit/actions/workflows/tests.yml/badge.svg) ![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen) ![license](https://img.shields.io/badge/license-MIT-green)

Six small, dependency-free Python tools for the everyday work of **evaluating and improving large language models**: catching hallucinations, ranking responses, red-teaming, scoring RAG pipelines, validating outputs and regression-testing prompts.

Each tool runs offline on its included example data in one command, and every one ships with unit tests that run in CI.

| Project | What it answers | Key techniques |
|---|---|---|
| [llm-hallucination-checker](llm-hallucination-checker) | Which claims in this answer are not backed by the source? | Claim splitting, lexical support, number/entity consistency |
| [llm-response-ranker](llm-response-ranker) | Which model do annotators prefer, and do they agree? | Rubric scoring, Elo, Bradley-Terry, Cohen's kappa |
| [llm-redteam-suite](llm-redteam-suite) | How often do jailbreak and injection attempts succeed? | Attack templates, refusal and leak detectors, attack success rate |
| [rag-eval-kit](rag-eval-kit) | Did retrieval find the right documents, and is the answer grounded? | Precision/Recall@k, MRR, nDCG, groundedness, answer F1 |
| [llm-output-guard](llm-output-guard) | Is this output safe to pass downstream? | JSON extraction, schema validation, PII detection and redaction |
| [prompt-regression-tester](prompt-regression-tester) | Did the new prompt or model break anything? | Assertion suites, run diffing, CI exit codes |

## Try it
```bash
git clone https://github.com/MartoNjiru/llm-evaluation-toolkit.git
cd llm-evaluation-toolkit/rag-eval-kit
python -m rageval examples/run.jsonl
```
Every folder has its own README with the exact command and sample output.

## Run all tests
```bash
for d in */; do (cd "$d" && python -m unittest discover -s tests); done
```

## Why these tools
They mirror the tasks in RLHF, red-teaming and AI-training projects: checking facts, comparing responses against a rubric, measuring annotator consistency and probing safety. Each metric is written from scratch so the logic is readable and easy to audit.

## Author
**Martin Njiru**, AI trainer and LLM evaluator based in Kenya. Available for evaluation, annotation and AI-training projects: martinnjiru35@gmail.com

Related: [Annotation & Translation QA](https://github.com/MartoNjiru/annotation-translation-qa) (inter-annotator agreement and Swahili-English MT evaluation).

MIT licensed.
