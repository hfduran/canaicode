import boto3

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics


class RawCopilotChatMetricsRepository:
    def __init__(self) -> None:
        self.table = boto3.resource("dynamodb").Table("raw_copilot_chat_metrics")  # type: ignore

    def put_item(self, commit: CopilotChatMetrics) -> None:
        item = commit.model_dump()
        self.table.put_item(Item=item)

    def get_item(self, id: str) -> CopilotChatMetrics | None:
        response = self.table.get_item(
            Key={
                "id": id,
            }
        )
        item = response.get("Item")
        if item:
            return CopilotChatMetrics.model_validate(item)
        return None
