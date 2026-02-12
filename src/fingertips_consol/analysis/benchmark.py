"""England benchmark comparison utilities."""

from __future__ import annotations

from fingertips_consol.models import BenchmarkClass


def classify_against_england(
    local_value: float,
    england_value: float,
    higher_is_better: bool,
    tolerance: float = 0.0,
) -> BenchmarkClass:
    if tolerance < 0:
        raise ValueError("tolerance must be >= 0")

    diff = local_value - england_value
    if abs(diff) <= tolerance:
        return BenchmarkClass.SIMILAR_TO_ENGLAND

    if higher_is_better:
        return BenchmarkClass.BETTER_THAN_ENGLAND if diff > 0 else BenchmarkClass.WORSE_THAN_ENGLAND

    return BenchmarkClass.BETTER_THAN_ENGLAND if diff < 0 else BenchmarkClass.WORSE_THAN_ENGLAND
