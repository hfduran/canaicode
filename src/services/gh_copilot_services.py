

from consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer


class GhCopilotServices:
    @staticmethod
    def summarize_metrics() -> None:
        consumer = GhCopilotConsumer()
        result = consumer.getMetrics()
        for entry in result:
            print(
                entry.date,
                entry.total_active_users,
            )