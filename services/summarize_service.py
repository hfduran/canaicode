from datetime import datetime
import time

from consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesDTO

REPO_PATH = "."


class SummaryService:
    @staticmethod
    def summarize_git_loc(start_date: datetime, end_date: datetime) -> None:
        st = time.time()
        result: list[ModifiedLinesDTO] = GitRepoConsumer(
            REPO_PATH
        ).count_modified_lines(start_date=start_date, end_date=end_date)
        et = time.time()
        for value in result:
            print(f"author: {value.author}")
            print(f"added lines: {value.added}")
            print(f"removed lines: {value.removed}")
            print("---")
        print("")
        print(f"time elapsed: {et - st}")
