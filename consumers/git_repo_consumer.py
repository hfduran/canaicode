from git import Repo
from datetime import datetime
from pydantic import BaseModel


class ModifiedLinesDTO(BaseModel):
    author: str
    added: int
    removed: int


class GitRepoConsumer:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def count_modified_lines(
        self, *, start_date: datetime, end_date: datetime
    ) -> list[ModifiedLinesDTO]:
        result: list[ModifiedLinesDTO] = []

        stats: dict[str, dict[str, int]] = {}

        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            author: str | None = commit.author.email
            if author is None:
                continue
            diff = commit.stats.total

            if author not in stats:
                stats[author] = {"added_lines": 0, "removed_lines": 0}

            stats[author]["added_lines"] += diff["insertions"]
            stats[author]["removed_lines"] += diff["deletions"]

        for author in stats:
            result.append(
                ModifiedLinesDTO(
                    author=author,
                    added=stats[author]["added_lines"],
                    removed=stats[author]["removed_lines"],
                )
            )

        return result
