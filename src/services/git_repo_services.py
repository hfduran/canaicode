from datetime import datetime
import time

from config.config import CONFIG
from consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesDTO


class GitRepoServices:
    @staticmethod
    def summarize_loc(start_date: datetime, end_date: datetime) -> None:
        st = time.time()
        result: list[ModifiedLinesDTO] = GitRepoConsumer(
            CONFIG.repo_path
        ).count_modified_lines(start_date=start_date, end_date=end_date)
        et = time.time()
        for value in result:
            print(f"author: {value.author}")
            print(f"added lines: {value.added}")
            print(f"removed lines: {value.removed}")
            print("---")
        print("")
        print(f"time elapsed: {et - st}")
