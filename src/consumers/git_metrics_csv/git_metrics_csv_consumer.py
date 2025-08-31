from datetime import datetime
from typing import List, TextIO
import csv
import uuid
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository


class GitCommitMetricsCsvConsumer:
  def execute(self, file_content: TextIO, user_id: str) -> List[CommitMetrics]:
    metrics: List[CommitMetrics] = []

    reader = csv.DictReader(file_content)
    for row in reader:
        commit = CommitMetrics(
            id=str(uuid.uuid4()),
            hash=row["hash"],
            repository=Repository(name=row["repository"], team=""),
            date=datetime.fromisoformat(row["date"]),
            author=Author(name=row["author"], teams=[]),
            language=row["language"],
            added_lines=int(row["added_lines"]),
            removed_lines=int(row["removed_lines"]),
            user_id=user_id
        )
        metrics.append(commit)

    return metrics