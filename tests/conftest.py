from datetime import datetime

import pytest

from src.domain.entities.author import Author
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.repository import Repository
from src.domain.entities.team import Team
from src.services.git_repo_services import ModifiedLinesWithAuthorDTO


@pytest.fixture
def git_repo_consumer_expected_response() -> list[ModifiedLinesWithAuthorDTO]:
    """
    Load the expected response for the GitRepoConsumer on example git repo.
    """
    import pickle

    __EXPECTED_RESPONSE_PATH = "./tests/data/git_repo_consumer_expected_response.pkl"
    with open(__EXPECTED_RESPONSE_PATH, "rb") as f:
        expected_response: list[ModifiedLinesWithAuthorDTO] = pickle.load(f)
    return expected_response


# ------------------- mock up data for unit tests ----------------


@pytest.fixture
def sample_repositories() -> list[Repository]:
    return [
        Repository(id="repo1A", name="Repo One A", team="Team A"),
        Repository(id="repo2A", name="Repo Two A", team="Team A"),
        Repository(id="repo3A", name="Repo Three A", team="Team A"),
        Repository(id="repo1B", name="Repo One B", team="Team B"),
        Repository(id="repo2B", name="Repo Two B", team="Team B"),
    ]


@pytest.fixture
def sample_authors() -> list[Author]:
    return [
        Author(name="John Doe", teams=["Repo One A", "Repo Two A", "Repo Three A"]),
        Author(name="Mary", teams=["Repo One B", "Repo Two B"]),
    ]


@pytest.fixture
def sample_commits(sample_repositories, sample_authors) -> list[CommitMetrics]:  # type: ignore
    return [
        CommitMetrics(
            hash="A1",
            repository=sample_repositories[0],  # type: ignore
            date=datetime(2024, 5, 1),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=100,
            removed_lines=20,
        ),
        CommitMetrics(
            hash="A2",
            repository=sample_repositories[1],  # type: ignore
            date=datetime(2024, 5, 2),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=50,
            removed_lines=10,
        ),
        CommitMetrics(
            hash="A3",
            repository=sample_repositories[2],  # type: ignore
            date=datetime(2024, 5, 3),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=30,
            removed_lines=20,
        ),
        CommitMetrics(
            hash="B1",
            repository=sample_repositories[3],  # type: ignore
            date=datetime(2024, 5, 1),
            author=sample_authors[1],  # type: ignore
            language="Python",
            added_lines=300,
            removed_lines=100,
        ),
        CommitMetrics(
            hash="B2",
            repository=sample_repositories[4],  # type: ignore
            date=datetime(2024, 5, 2),
            author=sample_authors[1],  # type: ignore
            language="Python",
            added_lines=250,
            removed_lines=80,
        ),
    ]


@pytest.fixture
def sample_copilot_metrics() -> list[CopilotCodeMetrics]:
    return [
        CopilotCodeMetrics(
            team=Team(id="team1", name="Team A"),
            date=datetime(2024, 5, 1),
            IDE="VSCode",
            copilot_model="GPT-4",
            language="Python",
            total_users=1,
            code_acceptances=10,
            code_suggestions=20,
            lines_accepted=150,
            lines_suggested=200,
            created_at=datetime(2024, 5, 1),
        ),
        CopilotCodeMetrics(
            team=Team(id="team2", name="Team B"),
            date=datetime(2024, 5, 2),
            IDE="VSCode",
            copilot_model="GPT-4",
            language="Python",
            total_users=3,
            code_acceptances=5,
            code_suggestions=15,
            lines_accepted=100,
            lines_suggested=150,
            created_at=datetime(2024, 5, 1),
        ),
    ]
