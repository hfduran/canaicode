from datetime import datetime
from io import BytesIO
from typing import List
import pandas as pd
import uuid
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository


class GitCommitMetricsXlsxConsumer:
  def execute(self, file_content: BytesIO, user_id: str) -> List[CommitMetrics]:
    metrics: List[CommitMetrics] = []

    sheets = pd.read_excel(file_content, sheet_name=None) # type: ignore
    for _, df in sheets.items():
      for _, row in df.iterrows():
        raw_date = row["date"]
        if isinstance(raw_date, str):
            date = datetime.fromisoformat(raw_date)
        else:
            date = raw_date
        commit = CommitMetrics(
            id=str(uuid.uuid4()),
            hash=row["hash"],
            repository=Repository(name=row["repository"], team=""),
            date=date, # type: ignore
            author=Author(name=row["author"], teams=[]),
            language=row["language"],
            added_lines=int(row["added_lines"]),
            removed_lines=int(row["removed_lines"]),
            user_id=user_id
        )
        metrics.append(commit)

    return metrics