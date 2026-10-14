import re

REFUSAL = re.compile(r"\b(I can(no|')t|I'm unable|I am unable|as an AI)\b", re.I)


def check_rules(text, max_words=None, min_words=None, must_include=(), banned=(), allow_refusal=False):
    """Return a list of human-readable rule violations."""
    problems = []
    words = len(text.split())
    if max_words and words > max_words:
        problems.append(f"too long: {words} words > {max_words}")
    if min_words and words < min_words:
        problems.append(f"too short: {words} words < {min_words}")
    low = text.lower()
    for term in must_include:
        if term.lower() not in low:
            problems.append(f"missing required term: {term}")
    for term in banned:
        if term.lower() in low:
            problems.append(f"contains banned term: {term}")
    if not allow_refusal and REFUSAL.search(text):
        problems.append("looks like a refusal")
    return problems
