from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    __REPO_PATH_ENV = "REPO_PATH"
    __DEFAULT_REPO_PATH = "."

    def __init__(self) -> None:
        self.repo_path: str = os.getenv(self.__REPO_PATH_ENV, self.__DEFAULT_REPO_PATH)

CONFIG = Config()