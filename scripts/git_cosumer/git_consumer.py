import os
import pandas as pd
from datetime import date, datetime, time, timedelta
from typing import List
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

    def get_commits_by_date(
        self, date: date
    ) -> List[CommitMetrics]:
        result: List[CommitMetrics] = []

        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date).date()
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
        raise ValueError("Data inválida. Use o formato YYYY-MM-DD.")


def main() -> None:
    repo_path = input("Digite o caminho do repositório Git: ").strip()
    start_date_str = input("Digite a data inicial (YYYY-MM-DD): ").strip()
    end_date_str = input("Digite a data final (YYYY-MM-DD): ").strip()

    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError as e:
        print(e)
        return

    if start_date > end_date:
        print("Erro: data inicial é posterior à data final.")
        return

    if not os.path.isdir(repo_path):
        print("Erro: caminho do repositório inválido.")
        return

    consumer = GitRepoConsumer(repo_path)
    all_commits: List[CommitMetrics] = []

    current_date = start_date
    while current_date <= end_date:
        print(f"Buscando commits em {current_date}...")
        commits = consumer.get_commits_by_date(current_date)
        all_commits.extend(commits)
        current_date += timedelta(days=1)

    if not all_commits:
        print("Nenhum commit encontrado no intervalo de datas.")
        return

    df = pd.DataFrame([c.model_dump() for c in all_commits]) 
    df.to_csv(f"commits_{start_date}_a_{end_date}.csv", index=False)
    print(f"Exportação finalizada com sucesso em: commits_{start_date}_a_{end_date}.csv")


if __name__ == "__main__":
    main()