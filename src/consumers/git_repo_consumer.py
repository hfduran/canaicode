from collections import defaultdict
import os
from git import Repo
from datetime import datetime
from pydantic import BaseModel


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

    def __get_language(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return self.__EXT_TO_LANG.get(ext, self.__DEFAULT_LANG)
