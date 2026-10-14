import re

PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "ke_phone": re.compile(r"(?<!\d)(?:\+254|254|0)(?:7|1)\d{8}(?!\d)"),
    "intl_phone": re.compile(r"\+\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}"),
    "card": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "ke_id": re.compile(r"\b(?:ID|id)\s*(?:no\.?|number)?\s*:?\s*\d{7,8}\b"),
}


def luhn(number):
    digits = [int(d) for d in re.sub(r"\D", "", number)][::-1]
    total = sum(d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2) for i, d in enumerate(digits))
    return total % 10 == 0


def find_pii(text):
    """Return a list of (kind, match) found in text. Card numbers must pass Luhn."""
    found, taken = [], []
    for kind, rx in PATTERNS.items():
        for m in rx.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue
            if kind == "card" and not luhn(m.group()):
                continue
            found.append((kind, m.group().strip()))
            taken.append(m.span())
    return found


def redact(text):
    for kind, value in find_pii(text):
        text = text.replace(value, f"[{kind.upper()}]")
    return text
