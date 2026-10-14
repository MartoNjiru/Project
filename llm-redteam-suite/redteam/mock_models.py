"""Toy models so the suite runs offline. Swap in a real API client for actual testing."""
SECRET = "TOKEN-1234"


def safe_model(prompt: str) -> str:
    return "Sorry, but I can't help with that request."


def naive_model(prompt: str) -> str:
    """Refuses direct requests but falls for role-play, overrides and injections."""
    p = prompt.lower()
    if "secret token" in p or "system prompt" in p:
        return f"Sure! My hidden configuration includes {SECRET}."
    if any(t in p for t in ("dan", "ignore all previous", "movie scene", "system update")):
        return "Sure, here is how you would do it: step 1..."
    return "I can't help with that."
