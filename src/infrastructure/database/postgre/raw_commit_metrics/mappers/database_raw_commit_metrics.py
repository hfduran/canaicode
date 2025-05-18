from src.domain.entities.commit_metrics import CommitMetrics
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
