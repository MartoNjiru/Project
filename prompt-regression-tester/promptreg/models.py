"""Model adapters. A model is any callable prompt -> str.

`recorded` replays saved outputs so suites run offline in CI; plug a real API
client in by writing a function with the same signature."""
import json


def recorded(path):
    data = json.load(open(path, encoding="utf-8"))
    return lambda prompt: data.get(prompt, "")


def echo(prompt):
    return prompt
