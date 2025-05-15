import boto3

from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics


class RawCopilotCodeMetricsRepository:
    def __init__(self) -> None:
        self.table = boto3.resource("dynamodb").Table("raw_copilot_code_metrics")  # type: ignore

    def put_item(self, code_metrics: CopilotCodeMetrics) -> None:
        item = code_metrics.model_dump()
        self.table.put_item(Item=item)

    def get_item(self, id: str) -> CopilotCodeMetrics | None:
        response = self.table.get_item(
            Key={
                "id": id,
            }
        )
        item = response.get("Item")
        if item:
            return CopilotCodeMetrics.model_validate(item)
        return None
