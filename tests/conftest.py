from datetime import datetime

import pytest

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository
from src.domain.entities.value_objects.team import Team


# ------------------- mock up data for unit tests ----------------


@pytest.fixture
def sample_repositories() -> list[Repository]:
    return [
        Repository(name="Repo One A", team="Team A"),
        Repository(name="Repo Two A", team="Team A"),
        Repository(name="Repo Three A", team="Team A"),
        Repository(name="Repo One B", team="Team B"),
        Repository(name="Repo Two B", team="Team B"),
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
            id="commit-a1",
            hash="A1",
            repository=sample_repositories[0],  # type: ignore
            date=datetime(2024, 5, 1),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=100,
            removed_lines=20,
            user_id="user1",
        ),
        CommitMetrics(
            id="commit-a2",
            hash="A2",
            repository=sample_repositories[1],  # type: ignore
            date=datetime(2024, 5, 2),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=50,
            removed_lines=10,
            user_id="user1",
        ),
        CommitMetrics(
            id="commit-a3",
            hash="A3",
            repository=sample_repositories[2],  # type: ignore
            date=datetime(2024, 5, 3),
            author=sample_authors[0],  # type: ignore
            language="Python",
            added_lines=30,
            removed_lines=20,
            user_id="user1",
        ),
        CommitMetrics(
            id="commit-b1",
            hash="B1",
            repository=sample_repositories[3],  # type: ignore
            date=datetime(2024, 5, 1),
            author=sample_authors[1],  # type: ignore
            language="Python",
            added_lines=300,
            removed_lines=100,
            user_id="user2",
        ),
        CommitMetrics(
            id="commit-b2",
            hash="B2",
            repository=sample_repositories[4],  # type: ignore
            date=datetime(2024, 5, 2),
            author=sample_authors[1],  # type: ignore
            language="Python",
            added_lines=250,
            removed_lines=80,
            user_id="user2",
        ),
    ]


@pytest.fixture
def sample_copilot_metrics() -> list[CopilotCodeMetrics]:
    return [
        CopilotCodeMetrics(
            id="id1",
            user_id="user1",
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
            id="id2",
            user_id="user2",
            team=Team(name="Team B"),
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
