import pytest
from datetime import datetime
from unittest.mock import Mock
import pandas as pd

from src.domain.use_cases.metrics_calculator import MetricsCalculator
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.value_objects.repository import Repository
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.team import Team


class TestMetricsCalculator:
    """Comprehensive unit tests for MetricsCalculator class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.sample_date = datetime(2024, 1, 1, 12, 0, 0)

        # Create sample entities
        self.sample_repository = Repository(id="repo-1", name="test-repo", team="team-alpha")
        self.sample_author = Author(name="John Doe", teams=["team-alpha"])
        self.sample_team = Team(id="team-1", name="team-alpha")

    def create_commit_metrics(self, added_lines=10, removed_lines=5, language="python", repo_name="test-repo"):
        """Helper method to create CommitMetrics instances."""
        repository = Repository(id="repo-1", name=repo_name, team="team-alpha")
        return CommitMetrics(
            id="commit-1",
            hash="abc123",
            repository=repository,
            date=self.sample_date,
            author=self.sample_author,
            language=language,
            added_lines=added_lines,
            removed_lines=removed_lines,
            user_id="user-1"
        )

    def create_copilot_code_metrics(self, lines_accepted=20, lines_suggested=40,
                                   code_acceptances=5, code_suggestions=10, language="python"):
        """Helper method to create CopilotCodeMetrics instances."""
        return CopilotCodeMetrics(
            id="copilot-1",
            team=self.sample_team,
            date=self.sample_date,
            IDE="vscode",
            copilot_model="gpt-4",
            user_id="user-1",
            language=language,
            total_users=1,
            code_acceptances=code_acceptances,
            code_suggestions=code_suggestions,
            lines_accepted=lines_accepted,
            lines_suggested=lines_suggested
        )

    # ================================ Gross Productivity Tests ================================

    def test_calculate_gross_productivity_with_valid_commits(self):
        """Test gross productivity calculation with valid commit data."""
        commits = [
            self.create_commit_metrics(added_lines=100, removed_lines=50),
            self.create_commit_metrics(added_lines=200, removed_lines=75),
            self.create_commit_metrics(added_lines=50, removed_lines=25)
        ]

        result = MetricsCalculator.calculate_gross_productivity(commits)

        expected = (100 + 50) + (200 + 75) + (50 + 25)  # 500
        assert result == expected

    def test_calculate_gross_productivity_with_empty_list(self):
        """Test gross productivity calculation with empty commit list."""
        result = MetricsCalculator.calculate_gross_productivity([])
        assert result == 0

    def test_calculate_gross_productivity_with_zero_lines(self):
        """Test gross productivity calculation with commits having zero lines."""
        commits = [
            self.create_commit_metrics(added_lines=0, removed_lines=0),
            self.create_commit_metrics(added_lines=0, removed_lines=0)
        ]

        result = MetricsCalculator.calculate_gross_productivity(commits)
        assert result == 0

    def test_calculate_gross_productivity_with_large_numbers(self):
        """Test gross productivity calculation with large line counts."""
        commits = [
            self.create_commit_metrics(added_lines=10000, removed_lines=5000)
        ]

        result = MetricsCalculator.calculate_gross_productivity(commits)
        assert result == 15000

    # ================================ Gross AI Usage Tests ================================

    def test_calculate_gross_use_of_AI_lines_with_valid_metrics(self):
        """Test gross AI lines calculation with valid metrics data."""
        metrics = [
            self.create_copilot_code_metrics(lines_accepted=100, lines_suggested=200),
            self.create_copilot_code_metrics(lines_accepted=150, lines_suggested=300),
            self.create_copilot_code_metrics(lines_accepted=50, lines_suggested=100)
        ]

        result = MetricsCalculator.calculate_gross_use_of_AI_lines(metrics)

        expected = 100 + 150 + 50  # 300
        assert result == expected

    def test_calculate_gross_use_of_AI_lines_with_empty_list(self):
        """Test gross AI lines calculation with empty metrics list."""
        result = MetricsCalculator.calculate_gross_use_of_AI_lines([])
        assert result == 0

    def test_calculate_gross_use_of_AI_with_valid_metrics(self):
        """Test gross AI usage calculation with valid metrics data."""
        metrics = [
            self.create_copilot_code_metrics(code_acceptances=10, code_suggestions=20),
            self.create_copilot_code_metrics(code_acceptances=15, code_suggestions=30),
            self.create_copilot_code_metrics(code_acceptances=5, code_suggestions=10)
        ]

        result = MetricsCalculator.calculate_gross_use_of_AI(metrics)

        expected = 10 + 15 + 5  # 30
        assert result == expected

    def test_calculate_gross_use_of_AI_with_empty_list(self):
        """Test gross AI usage calculation with empty metrics list."""
        result = MetricsCalculator.calculate_gross_use_of_AI([])
        assert result == 0

    # ================================ Relative AI Usage Tests ================================

    def test_calculate_relative_use_of_AI_lines_with_valid_metrics(self):
        """Test relative AI lines calculation with valid metrics data."""
        metrics = [
            self.create_copilot_code_metrics(lines_accepted=50, lines_suggested=100),
            self.create_copilot_code_metrics(lines_accepted=30, lines_suggested=60)
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI_lines(metrics)

        # Total accepted: 80, Total suggested: 160, Ratio: 0.5
        expected = 80.0 / 160.0
        assert result == expected

    def test_calculate_relative_use_of_AI_lines_with_zero_suggested(self):
        """Test relative AI lines calculation when total suggested is zero."""
        metrics = [
            self.create_copilot_code_metrics(lines_accepted=0, lines_suggested=0)
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI_lines(metrics)
        assert result == 0.0

    def test_calculate_relative_use_of_AI_lines_with_empty_list(self):
        """Test relative AI lines calculation with empty metrics list."""
        result = MetricsCalculator.calculate_relative_use_of_AI_lines([])
        assert result == 0.0

    def test_calculate_relative_use_of_AI_with_valid_metrics(self):
        """Test relative AI usage calculation with valid metrics data."""
        metrics = [
            self.create_copilot_code_metrics(code_acceptances=25, code_suggestions=100),
            self.create_copilot_code_metrics(code_acceptances=15, code_suggestions=60)
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI(metrics)

        # Total accepted: 40, Total suggested: 160, Ratio: 0.25
        expected = 40.0 / 160.0
        assert result == expected

    def test_calculate_relative_use_of_AI_with_zero_suggested(self):
        """Test relative AI usage calculation when total suggested is zero."""
        metrics = [
            self.create_copilot_code_metrics(code_acceptances=0, code_suggestions=0)
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI(metrics)
        assert result == 0.0

    def test_calculate_relative_use_of_AI_with_empty_list(self):
        """Test relative AI usage calculation with empty metrics list."""
        result = MetricsCalculator.calculate_relative_use_of_AI([])
        assert result == 0.0

    # ================================ Grouped Calculations Tests ================================

    def test_calculate_gross_productivity_grouped_by_language(self):
        """Test gross productivity calculation grouped by language."""
        commits = [
            self.create_commit_metrics(added_lines=100, removed_lines=50, language="python"),
            self.create_commit_metrics(added_lines=80, removed_lines=20, language="python"),
            self.create_commit_metrics(added_lines=60, removed_lines=40, language="javascript"),
            self.create_commit_metrics(added_lines=120, removed_lines=30, language="javascript")
        ]

        repositories = [self.sample_repository]

        result = MetricsCalculator.calculate_gross_productivity_grouped_by(
            commits, repositories, ["language"]
        )

        # Convert to dict for easier testing
        result_dict = result.set_index('language')['gross_productivity'].to_dict()

        # Python: (100+50) + (80+20) = 250
        # JavaScript: (60+40) + (120+30) = 250
        assert result_dict["python"] == 250
        assert result_dict["javascript"] == 250

    def test_calculate_gross_productivity_grouped_by_team(self):
        """Test gross productivity calculation grouped by team."""
        repo1 = Repository(id="repo-1", name="repo1", team="team-alpha")
        repo2 = Repository(id="repo-2", name="repo2", team="team-beta")

        commits = [
            CommitMetrics(
                id="1", hash="abc1", repository=repo1, date=self.sample_date,
                author=self.sample_author, language="python",
                added_lines=100, removed_lines=50, user_id="user-1"
            ),
            CommitMetrics(
                id="2", hash="abc2", repository=repo2, date=self.sample_date,
                author=self.sample_author, language="python",
                added_lines=80, removed_lines=20, user_id="user-1"
            )
        ]

        repositories = [repo1, repo2]

        result = MetricsCalculator.calculate_gross_productivity_grouped_by(
            commits, repositories, ["team"]
        )

        result_dict = result.set_index('team')['gross_productivity'].to_dict()

        # team-alpha: 100+50 = 150
        # team-beta: 80+20 = 100
        assert result_dict["team-alpha"] == 150
        assert result_dict["team-beta"] == 100

    def test_calculate_gross_productivity_grouped_by_invalid_column(self):
        """Test gross productivity calculation with invalid group_by column."""
        commits = [self.create_commit_metrics()]
        repositories = [self.sample_repository]

        with pytest.raises(ValueError, match="Invalid group_by columns"):
            MetricsCalculator.calculate_gross_productivity_grouped_by(
                commits, repositories, ["invalid_column"]
            )

    def test_calculate_gross_use_of_AI_grouped_by_language(self):
        """Test gross AI usage calculation grouped by language."""
        metrics = [
            self.create_copilot_code_metrics(lines_accepted=100, language="python"),
            self.create_copilot_code_metrics(lines_accepted=80, language="python"),
            self.create_copilot_code_metrics(lines_accepted=60, language="javascript"),
            self.create_copilot_code_metrics(lines_accepted=40, language="javascript")
        ]

        result = MetricsCalculator.calculate_gross_use_of_AI_grouped_by(
            metrics, ["language"]
        )

        result_dict = result.set_index('language')['gross_use_of_AI'].to_dict()

        # Python: 100 + 80 = 180
        # JavaScript: 60 + 40 = 100
        assert result_dict["python"] == 180
        assert result_dict["javascript"] == 100

    def test_calculate_gross_use_of_AI_grouped_by_invalid_column(self):
        """Test gross AI usage calculation with invalid group_by column."""
        metrics = [self.create_copilot_code_metrics()]

        with pytest.raises(ValueError, match="Invalid group_by columns"):
            MetricsCalculator.calculate_gross_use_of_AI_grouped_by(
                metrics, ["invalid_column"]
            )

    def test_calculate_relative_use_of_AI_grouped_by_language(self):
        """Test relative AI usage calculation grouped by language."""
        metrics = [
            self.create_copilot_code_metrics(
                lines_accepted=50, lines_suggested=100, language="python"
            ),
            self.create_copilot_code_metrics(
                lines_accepted=30, lines_suggested=100, language="python"
            ),
            self.create_copilot_code_metrics(
                lines_accepted=20, lines_suggested=100, language="javascript"
            ),
            self.create_copilot_code_metrics(
                lines_accepted=60, lines_suggested=100, language="javascript"
            )
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI_grouped_by(
            metrics, ["language"]
        )

        result_dict = result.set_index('language')['relative_use_of_AI'].to_dict()

        # Python: (50+30)/(100+100) = 80/200 = 0.4
        # JavaScript: (20+60)/(100+100) = 80/200 = 0.4
        assert result_dict["python"] == 0.4
        assert result_dict["javascript"] == 0.4

    def test_calculate_relative_use_of_AI_grouped_by_with_zero_suggested(self):
        """Test relative AI usage calculation grouped by language with zero suggested."""
        metrics = [
            self.create_copilot_code_metrics(
                lines_accepted=0, lines_suggested=0, language="python"
            ),
            self.create_copilot_code_metrics(
                lines_accepted=50, lines_suggested=100, language="javascript"
            )
        ]

        result = MetricsCalculator.calculate_relative_use_of_AI_grouped_by(
            metrics, ["language"]
        )

        result_dict = result.set_index('language')['relative_use_of_AI'].to_dict()

        # Python: 0/0 = 0 (handled by the condition)
        # JavaScript: 50/100 = 0.5
        assert result_dict["python"] == 0
        assert result_dict["javascript"] == 0.5

    def test_calculate_relative_use_of_AI_grouped_by_invalid_column(self):
        """Test relative AI usage calculation with invalid group_by column."""
        metrics = [self.create_copilot_code_metrics()]

        with pytest.raises(ValueError, match="Invalid group_by columns"):
            MetricsCalculator.calculate_relative_use_of_AI_grouped_by(
                metrics, ["invalid_column"]
            )

    # ================================ Edge Cases and Integration Tests ================================

    def test_integration_all_metrics_calculation(self):
        """Integration test combining all metric calculations."""
        # Create sample data
        commits = [
            self.create_commit_metrics(added_lines=200, removed_lines=100),
            self.create_commit_metrics(added_lines=150, removed_lines=50)
        ]

        copilot_metrics = [
            self.create_copilot_code_metrics(
                lines_accepted=80, lines_suggested=160,
                code_acceptances=20, code_suggestions=40
            ),
            self.create_copilot_code_metrics(
                lines_accepted=120, lines_suggested=240,
                code_acceptances=30, code_suggestions=60
            )
        ]

        # Test all calculations
        gross_productivity = MetricsCalculator.calculate_gross_productivity(commits)
        gross_ai_lines = MetricsCalculator.calculate_gross_use_of_AI_lines(copilot_metrics)
        gross_ai_usage = MetricsCalculator.calculate_gross_use_of_AI(copilot_metrics)
        relative_ai_lines = MetricsCalculator.calculate_relative_use_of_AI_lines(copilot_metrics)
        relative_ai_usage = MetricsCalculator.calculate_relative_use_of_AI(copilot_metrics)

        # Verify results
        assert gross_productivity == 500  # (200+100) + (150+50)
        assert gross_ai_lines == 200      # 80 + 120
        assert gross_ai_usage == 50       # 20 + 30
        assert relative_ai_lines == 0.5   # 200/400
        assert relative_ai_usage == 0.5   # 50/100

    def test_empty_dataframe_handling(self):
        """Test that all methods handle empty data gracefully."""
        empty_commits = []
        empty_metrics = []
        empty_repositories = []

        # Test all methods with empty data
        assert MetricsCalculator.calculate_gross_productivity(empty_commits) == 0
        assert MetricsCalculator.calculate_gross_use_of_AI_lines(empty_metrics) == 0
        assert MetricsCalculator.calculate_gross_use_of_AI(empty_metrics) == 0
        assert MetricsCalculator.calculate_relative_use_of_AI_lines(empty_metrics) == 0.0
        assert MetricsCalculator.calculate_relative_use_of_AI(empty_metrics) == 0.0

    def test_single_item_calculations(self):
        """Test calculations with single items."""
        single_commit = [self.create_commit_metrics(added_lines=100, removed_lines=50)]
        single_metric = [self.create_copilot_code_metrics(
            lines_accepted=40, lines_suggested=80,
            code_acceptances=10, code_suggestions=20
        )]

        assert MetricsCalculator.calculate_gross_productivity(single_commit) == 150
        assert MetricsCalculator.calculate_gross_use_of_AI_lines(single_metric) == 40
        assert MetricsCalculator.calculate_gross_use_of_AI(single_metric) == 10
        assert MetricsCalculator.calculate_relative_use_of_AI_lines(single_metric) == 0.5
        assert MetricsCalculator.calculate_relative_use_of_AI(single_metric) == 0.5

    def test_data_type_consistency(self):
        """Test that return types are consistent with expected types."""
        commits = [self.create_commit_metrics(added_lines=100, removed_lines=50)]
        metrics = [self.create_copilot_code_metrics(
            lines_accepted=40, lines_suggested=80,
            code_acceptances=10, code_suggestions=20
        )]

        # Test return types
        gross_productivity = MetricsCalculator.calculate_gross_productivity(commits)
        gross_ai_lines = MetricsCalculator.calculate_gross_use_of_AI_lines(metrics)
        gross_ai_usage = MetricsCalculator.calculate_gross_use_of_AI(metrics)
        relative_ai_lines = MetricsCalculator.calculate_relative_use_of_AI_lines(metrics)
        relative_ai_usage = MetricsCalculator.calculate_relative_use_of_AI(metrics)

        assert isinstance(gross_productivity, int)
        assert isinstance(gross_ai_lines, int)
        assert isinstance(gross_ai_usage, int)
        assert isinstance(relative_ai_lines, float)
        assert isinstance(relative_ai_usage, float)

        # Test grouped calculations return DataFrames
        repositories = [self.sample_repository]
        grouped_result = MetricsCalculator.calculate_gross_productivity_grouped_by(
            commits, repositories, ["language"]
        )
        assert isinstance(grouped_result, pd.DataFrame)