import pytest

from src.domain.use_cases.metrics_calculator import MetricsCalculator


def test_calculate_gross_productivity(sample_commits):  # type: ignore
    result = MetricsCalculator.calculate_gross_productivity(sample_commits)  # type: ignore
    assert result == 960


def test_calculate_gross_use_of_ai(sample_copilot_metrics):  # type: ignore
    result = MetricsCalculator.calculate_gross_use_of_AI(sample_copilot_metrics)  # type: ignore
    # Sum of code_acceptances: 10 + 5 = 15
    assert result == 15


def test_calculate_relative_use_of_ai(sample_copilot_metrics):  # type: ignore
    result = MetricsCalculator.calculate_relative_use_of_AI(sample_copilot_metrics)  # type: ignore
    # Ratio of code_acceptances / code_suggestions: (10 + 5) / (20 + 15) = 15 / 35
    expected = (10 + 5) / (20 + 15)
    assert pytest.approx(result, 0.001) == expected  # type: ignore
