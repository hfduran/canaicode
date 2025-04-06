from datetime import datetime
import pickle
from typing import Iterator
from git import Repo
from pytest import MonkeyPatch
from git.objects.commit import Commit

from src.consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesDTO

__EXPECTED_RESPONSE_PATH = "./tests/data/git_repo_consumer_expected_response.pkl"
__REPO_MONKEYPATCH_PATH = "src.consumers.git_repo_consumer.Repo"


class FakeRepo:
    def __init__(self, repo_path: str):
        with open("./tests/data/repo_example.pkl", "rb") as f:
            self.repo: Repo = pickle.load(f)

    def iter_commits(self, *, since: datetime, until: datetime) -> Iterator[Commit]:
        return self.repo.iter_commits(since=since, until=until)


def test_git_repo_consumer(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(__REPO_MONKEYPATCH_PATH, FakeRepo)

    response: list[ModifiedLinesDTO] = GitRepoConsumer("whatever").count_modified_lines(
        start_date=datetime(2024, 1, 1), end_date=datetime(2025, 10, 10)
    )

    with open(__EXPECTED_RESPONSE_PATH, "rb") as f:
        expected_response: list[ModifiedLinesDTO] = pickle.load(f)
    assert len(response) == len(expected_response)
    assert all(
        [
            r1.model_dump() == r2.model_dump()
            for r1, r2 in zip(response, expected_response)
        ]
    ), f"Expected {expected_response} but got {response}"
