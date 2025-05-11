import boto3

from src.domain.entities.commit_metrics import CommitMetrics


class RawCommitMetricsRepository:
    def __init__(self) -> None:
        self.table = boto3.resource("dynamodb").Table("raw_commit_metrics")  # type: ignore

    def put_item(self, commit: CommitMetrics) -> None:
        item = commit.model_dump()
        self.table.put_item(Item=item)

    def get_item(self, id: str) -> CommitMetrics | None:
        response = self.table.get_item(
            Key={
                "id": id,
            }
        )
        item = response.get("Item")
        if item:
            return CommitMetrics.model_validate(item)
        return None
