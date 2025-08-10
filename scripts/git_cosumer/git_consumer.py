import os
import tempfile
import shutil
import pandas as pd
from datetime import date, datetime, time, timedelta
from typing import List, Dict
from git import Repo
from pydantic import BaseModel


class CommitMetrics(BaseModel):
    hash: str
    repository: str
    date: datetime
    author: str | None
    language: str
    added_lines: int
    removed_lines: int


class GitRepoConsumer:
    __DEFAULT_LANG = "Other"
    __EXT_TO_LANG = {
        ".py": "Python", ".ts": "TypeScript", ".js": "JavaScript",
        ".tsx": "TypeScript", ".jsx": "JavaScript", ".java": "Java",
        ".rb": "Ruby", ".go": "Go", ".rs": "Rust", ".cpp": "C++",
        ".c": "C", ".cs": "C#", ".php": "PHP", ".html": "HTML",
        ".css": "CSS", ".json": "JSON", ".txt": "Plain Text",
        ".md": "Markdown"
    }
    __NULL_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def get_commits_by_date(self, date: date) -> List[CommitMetrics]:
        result: List[CommitMetrics] = []

        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date).date()
            if commit_date != date:
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
                        added_lines=int(added),
                        author=author,
                        date=datetime.combine(commit_date, time.min),
                        hash=commit.hexsha,
                        language=language,
                        removed_lines=int(removed),
                        repository=os.path.basename(os.path.normpath(self.repo_path)),
                    )
                )
        return result

    def __get_language(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return self.__EXT_TO_LANG.get(ext, self.__DEFAULT_LANG)


def parse_date(input_str: str) -> date:
    try:
        return datetime.strptime(input_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date. Use the format YYYY-MM-DD.")


def process_repository(repo_url: str, start_date: date, end_date: date) -> List[CommitMetrics]:
    temp_dir = tempfile.mkdtemp()
    repo_name = os.path.splitext(os.path.basename(repo_url.rstrip("/")))[0]
    repo_path = os.path.join(temp_dir, repo_name)

    try:
        print(f"Clonando {repo_url}...")
        Repo.clone_from(repo_url, repo_path)

        consumer = GitRepoConsumer(repo_path)
        all_commits: List[CommitMetrics] = []

        current_date = start_date
        while current_date <= end_date:
            print(f"Fetching commits from {repo_name} on {current_date}...")
            commits = consumer.get_commits_by_date(current_date)
            all_commits.extend(commits)
            current_date += timedelta(days=1)

        return all_commits
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main() -> None:
    urls_file = input("Enter the path to the .txt file with repository URLs: ").strip()
    start_date_str = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date_str = input("Enter the end date (YYYY-MM-DD): ").strip()

    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError as e:
        print(e)
        return

    if start_date > end_date:
        print("Error: Start date is later than end date.")
        return

    if not os.path.isfile(urls_file):
        print("Error: Invalid file path.")
        return

    repo_data: Dict[str, List[CommitMetrics]] = {}
    with open(urls_file, "r", encoding="utf-8") as f:
        repo_urls = [line.strip() for line in f if line.strip()]

    for repo_url in repo_urls:
        commits = process_repository(repo_url, start_date, end_date)
        if commits:
            repo_name = commits[0].repository
            repo_data[repo_name] = commits

    if not repo_data:
        print("No commits found in the date range.")
        return

    output_file = f"commits_{start_date}_to_{end_date}.xlsx"
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for repo_name, commits in repo_data.items():
            df = pd.DataFrame([c.model_dump() for c in commits])
            df.to_excel(writer, sheet_name=repo_name[:31], index=False)

    print(f"Export completed successfully: {output_file}")


if __name__ == "__main__":
    main()
