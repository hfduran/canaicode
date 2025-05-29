from datetime import datetime
from typing import cast

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository
from src.infrastructure.database.postgre.raw_commit_metrics.dtos.model import (
    RawCommitMetrics,
)


class DatabaseRawCommitMetricsMapper:
    @staticmethod
    def to_database(commit_metrics: CommitMetrics) -> RawCommitMetrics:
        return RawCommitMetrics(
            id=commit_metrics.id,
            hash=commit_metrics.hash,
            repository_name=commit_metrics.repository.name,
            repository_team=commit_metrics.repository.team,
            date=commit_metrics.date,
            author_name=commit_metrics.author.name,
            author_teams=",".join(str(item) for item in commit_metrics.author.teams),
            language=commit_metrics.language,
            added_lines=commit_metrics.added_lines,
            removed_lines=commit_metrics.removed_lines,
            created_at=commit_metrics.created_at,
        )

    @staticmethod
    def to_domain(db_schema: RawCommitMetrics) -> CommitMetrics:
        repository = Repository(
            name=cast(str, db_schema.repository_name),
            team=cast(str, db_schema.repository_team),
        )

        author = Author(
            name=cast(str, db_schema.author_name),
            teams=cast(str, db_schema.author_teams).split(),
        )

        return CommitMetrics(
            id=cast(str, db_schema.id),
            hash=cast(str, db_schema.hash),
            repository=repository,
            date=cast(datetime, db_schema.date),
            author=author,
            language=cast(str, db_schema.language),
            added_lines=cast(int, db_schema.added_lines),
            removed_lines=cast(int, db_schema.removed_lines),
            created_at=cast(datetime, db_schema.created_at),
        )
