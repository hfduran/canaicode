from src.services.git_repo_services import ModifiedLinesWithAuthorDTO
import pytest


@pytest.fixture
def git_repo_consumer_expected_response() -> list[ModifiedLinesWithAuthorDTO]:
    """
    Load the expected response for the GitRepoConsumer on example git repo.
    """
    import pickle

    __EXPECTED_RESPONSE_PATH = "./tests/data/git_repo_consumer_expected_response.pkl"
    with open(__EXPECTED_RESPONSE_PATH, "rb") as f:
        expected_response: list[ModifiedLinesWithAuthorDTO] = pickle.load(f)
    return expected_response
