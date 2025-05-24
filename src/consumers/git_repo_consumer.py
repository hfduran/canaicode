import os
import uuid
from collections import defaultdict
from datetime import datetime
from typing import List

from git import Repo
from pydantic import BaseModel

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository


class ModifiedLinesDTO(BaseModel):
    added: int = 0
    removed: int = 0


class ModifiedLinesWithAuthorDTO(BaseModel):
    author: str
    added: int
    removed: int


class GitRepoConsumer:
    __DEFAULT_LANG = "Other"
    __EXT_TO_LANG = {
        ".py": "Python",
        ".ts": "TypeScript",
        ".js": "JavaScript",
        ".tsx": "TypeScript",
        ".jsx": "JavaScript",
        ".java": "Java",
        ".rb": "Ruby",
        ".go": "Go",
        ".rs": "Rust",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".txt": "Plain Text",
        ".md": "Markdown",
    }
    __NULL_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def modified_lines_by_language(
        self, start_date: datetime, end_date: datetime
    ) -> dict[str, ModifiedLinesDTO]:
        result: dict[str, ModifiedLinesDTO] = defaultdict(
            lambda: ModifiedLinesDTO(added=0, removed=0)
        )

        for commit in self.repo.iter_commits():
            commit_dt = datetime.fromtimestamp(commit.committed_date)
            if not (start_date <= commit_dt <= end_date):
                continue

            if not commit.parents:
                diff = self.repo.git.diff(self.__NULL_TREE, commit.hexsha, "--numstat")
            else:
                diff = self.repo.git.diff(
                    commit.parents[0].hexsha, commit.hexsha, "--numstat"
                )

            for line in diff.splitlines():
                parts = line.strip().split("\t")
                if len(parts) != 3:
                    continue

                added, removed, filename = parts
                if added == "-" or removed == "-":
                    continue

                lang = self.__get_language(filename)
                result[lang].added += int(added)
                result[lang].removed += int(removed)
        return result

    def modified_lines_by_author(
        self, *, start_date: datetime, end_date: datetime
    ) -> list[ModifiedLinesWithAuthorDTO]:
        result: list[ModifiedLinesWithAuthorDTO] = []

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
                ModifiedLinesWithAuthorDTO(
                    author=author,
                    added=stats[author]["added_lines"],
                    removed=stats[author]["removed_lines"],
                )
            )

        return result

    def get_commits_by_date(
        self, date: datetime, team_name: str
    ) -> List[CommitMetrics]:
        result: List[CommitMetrics] = []

        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date)
            if not (commit_date == date):
                continue

            if not commit.parents:
                diff = self.repo.git.diff(self.__NULL_TREE, commit.hexsha, "--numstat")
            else:
                diff = self.repo.git.diff(
                    commit.parents[0].hexsha, commit.hexsha, "--numstat"
                )

            author: str | None = commit.author.email

            for line in diff.splitlines():
                parts = line.strip().split("\t")
                if len(parts) != 3:
                    continue

                added, removed, filename = parts
                if added == "-":
                    added = 0
                if removed == "-":
                    removed = 0

                language = self.__get_language(filename)
                result.append(
                    CommitMetrics(
                        id=str(uuid.uuid4()),
                        added_lines=int(added),
                        author=Author(
                            name=author, teams=[]
                        ),  # TODO: ver como associar o autor ao time (usar 'default' para os primeiros testes?)
                        date=commit_date,
                        hash=commit.hexsha,
                        language=language,
                        removed_lines=int(removed),
                        repository=Repository(name=self.repo_path, team=team_name),
                    )
                )
        return result

    def __get_language(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return self.__EXT_TO_LANG.get(ext, self.__DEFAULT_LANG)
