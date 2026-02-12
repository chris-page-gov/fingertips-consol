import pytest

from fingertips_consol.analysis.trends import classify_trend
from fingertips_consol.models import TrendClass


def test_classify_trend_improving_when_upward_direction_and_value_rises() -> None:
    assert classify_trend(12.0, 10.0, "up") == TrendClass.IMPROVING


def test_classify_trend_stable_within_tolerance() -> None:
    assert classify_trend(10.01, 10.0, "up", tolerance=0.05) == TrendClass.STABLE


def test_classify_trend_raises_on_invalid_direction() -> None:
    with pytest.raises(ValueError):
        classify_trend(11.0, 10.0, "sideways")


def test_classify_trend_raises_on_negative_tolerance() -> None:
    with pytest.raises(ValueError):
        classify_trend(11.0, 10.0, "up", tolerance=-0.01)


def test_classify_trend_improving_when_downward_direction_and_value_falls() -> None:
    assert classify_trend(9.0, 10.0, "down") == TrendClass.IMPROVING
