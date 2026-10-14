"""redteam: a small harness for adversarial (red-team) testing of chat models."""
from .attacks import ATTACKS, build_prompts
from .detectors import is_refusal, leaks_secret
from .runner import run_suite, SuiteReport

__all__ = ["ATTACKS", "build_prompts", "is_refusal", "leaks_secret", "run_suite", "SuiteReport"]
__version__ = "0.1.0"
