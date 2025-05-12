import pytest
from src.domain.entities.use_cases.metrics_calculator import MetricsCalculator

def test_calculate_gross_productivity(sample_commits): # type: ignore
    result = MetricsCalculator.calculate_gross_productivity(sample_commits) # type: ignore
    assert result == 960

def test_calculate_gross_use_of_ai(sample_copilot_metrics): # type: ignore
    result = MetricsCalculator.calculate_gross_use_of_AI(sample_copilot_metrics) # type: ignore
    assert result == 250

def test_calculate_relative_use_of_ai(sample_copilot_metrics): # type: ignore
    result = MetricsCalculator.calculate_relative_use_of_AI(sample_copilot_metrics) # type: ignore
    expected = (150 + 100) / (200 + 150)
    assert pytest.approx(result, 0.001) == expected # type: ignore