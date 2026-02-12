import pytest

from fingertips_consol.analysis.benchmark import classify_against_england
from fingertips_consol.models import BenchmarkClass


def test_classify_against_england_better_when_higher_is_better() -> None:
    result = classify_against_england(local_value=88.0, england_value=80.0, higher_is_better=True)
    assert result == BenchmarkClass.BETTER_THAN_ENGLAND


def test_classify_against_england_similar_within_tolerance() -> None:
    result = classify_against_england(
        local_value=80.04,
        england_value=80.0,
        higher_is_better=True,
        tolerance=0.05,
    )
    assert result == BenchmarkClass.SIMILAR_TO_ENGLAND


def test_classify_against_england_raises_for_negative_tolerance() -> None:
    with pytest.raises(ValueError):
        classify_against_england(80.0, 78.0, higher_is_better=True, tolerance=-0.1)


def test_classify_against_england_better_when_lower_is_better() -> None:
    result = classify_against_england(local_value=4.0, england_value=6.0, higher_is_better=False)
    assert result == BenchmarkClass.BETTER_THAN_ENGLAND
