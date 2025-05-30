import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    __REPO_PATH_ENV = "REPO_PATH"
    __GH_COPILOT_METRICS_FILE_PATH_ENV = "GH_COPILOT_METRICS_FILE_PATH"

    __DEFAULT_REPO_PATH = "."

    def __init__(self) -> None:
        self.repo_path: str = os.getenv(self.__REPO_PATH_ENV, self.__DEFAULT_REPO_PATH)
        self.gh_copilot_metrics_file_path: str = os.getenv(
            self.__GH_COPILOT_METRICS_FILE_PATH_ENV, ""
        )


CONFIG = Config()
