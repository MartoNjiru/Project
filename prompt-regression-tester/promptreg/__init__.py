"""Regression testing for prompts and model versions."""
from .assertions import run_assertion
from .runner import run_suite, diff_runs
__all__ = ["run_assertion", "run_suite", "diff_runs"]
