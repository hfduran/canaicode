from datetime import datetime, date

from config.config import CONFIG
from consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesDTO
from typer import echo


class GitRepoServices:
    @staticmethod
    def summarize_loc(start_date: date, end_date: date) -> None:
        result: list[ModifiedLinesDTO] = GitRepoConsumer(
            CONFIG.repo_path
        ).count_modified_lines(
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
