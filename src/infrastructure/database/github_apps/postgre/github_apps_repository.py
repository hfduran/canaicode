from sqlalchemy.orm import Session

from src.domain.entities.github_app import GitHubApp
from src.infrastructure.database.github_apps.postgre.dtos.model import GitHubAppDbSchema
from src.infrastructure.database.github_apps.postgre.mappers.database_github_apps import DatabaseGitHubAppsMapper


class GitHubAppsRepository:
  def __init__(self, db: Session) -> None:
        self.db = db

  def create(self, github_app: GitHubApp) -> None:
      record_to_save = DatabaseGitHubAppsMapper.to_database(
          github_app
      )

      self.db.add(record_to_save)
      self.db.commit()

  def find_by_id(
      self,
      github_app_id: str
  ) -> GitHubApp | None:
      query = self.db.query(GitHubAppDbSchema)

      record = query.filter(GitHubAppDbSchema.id == github_app_id).first()

      if(not record):
          return None

      return DatabaseGitHubAppsMapper.to_domain(record)