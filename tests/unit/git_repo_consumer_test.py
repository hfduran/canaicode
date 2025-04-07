from datetime import datetime

from src.consumers.git_repo_consumer import GitRepoConsumer, ModifiedLinesWithAuthorDTO

__EXAMPLE_REPO_PATH = "./tests/data/example_git_repo"


def test_git_repo_consumer(
    git_repo_consumer_expected_response: list[ModifiedLinesWithAuthorDTO],
) -> None:
    expected_response = git_repo_consumer_expected_response

    consumer = GitRepoConsumer(__EXAMPLE_REPO_PATH)

    response: list[ModifiedLinesWithAuthorDTO] = consumer.modified_lines_by_author(
        start_date=datetime(2024, 1, 1), end_date=datetime(2025, 10, 10)
    )

    assert len(response) == len(expected_response)
    assert all(
        [
            r1.model_dump() == r2.model_dump()
            for r1, r2 in zip(response, expected_response)
        ]
    ), f"Expected {expected_response} but got {response}"
