from datetime import datetime, date

from config.config import CONFIG
from consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesWithAuthorDTO
from typer import echo


class GitRepoServices:
    @staticmethod
    def summarize_loc_by_author(start_date: date, end_date: date) -> None:
        result: list[ModifiedLinesWithAuthorDTO] = GitRepoConsumer(
            CONFIG.repo_path
        ).modified_lines_by_author(
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=datetime.combine(end_date, datetime.min.time()),
        )
        for value in result:
            echo()
            echo(f"author: {value.author}")
            echo(f"added lines: {value.added}")
            echo(f"removed lines: {value.removed}")
            echo("---")
        echo()

    @staticmethod
    def summarize_loc_by_language(start_date: date, end_date: date) -> None:
        result = GitRepoConsumer(CONFIG.repo_path).modified_lines_by_language(
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=datetime.combine(end_date, datetime.min.time()),
        )

        for lang, stats in result.items():
            echo()
            echo(f"Language: {lang}")
            echo(f"Added lines: {stats.added}")
            echo(f"Removed lines: {stats.removed}")
            echo("---")
        echo()
