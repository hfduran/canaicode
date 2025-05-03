import pandas as pd # type: ignore
from typing import List

# from src.domain.entities.entity import Entity
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
# from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
# from src.domain.entities.copilot_metrics import CopilotMetrics
from src.domain.entities.repository import Repository
# from src.domain.entities.author import Author

class MetricsCalculator:

    # ================================ Gross calculations ================================

    @staticmethod
    def calculate_gross_productivity(commits: List[CommitMetrics]) -> int:
        if not commits:
            return 0
        
        df = pd.DataFrame([c.__dict__ for c in commits])
        return int(df['added_lines'].sum() + df['removed_lines'].sum())

    @staticmethod
    def calculate_gross_use_of_AI(metrics: List[CopilotCodeMetrics]) -> int:
        if not metrics:
            return 0

        df = pd.DataFrame([m.__dict__ for m in metrics])
        return int(df['lines_accepted'].sum())

    @staticmethod
    def calculate_relative_use_of_AI(metrics: List[CopilotCodeMetrics]) -> float:
        if not metrics:
            return 0.0

        df = pd.DataFrame([m.__dict__ for m in metrics])
        total_suggested = df['lines_suggested'].sum()
        total_accepted = df['lines_accepted'].sum()

        if total_suggested == 0:
            return 0.0

        return float(total_accepted / total_suggested)
    
    # ================================ Grouping by calculations ================================

    @staticmethod
    def calculate_gross_productivity_grouped_by(
            commits: List[CommitMetrics],
            repositories: List[Repository],
            group_by: List[str]
        ) -> pd.DataFrame:
        allowed = {"repository_id", "language", "team"}
        if not set(group_by).issubset(allowed):
            raise ValueError(f"Invalid group_by columns: {group_by}. Allowed: {allowed}")

        df_commits = pd.DataFrame([c.model_dump() for c in commits])
        df_repos = pd.DataFrame([r.model_dump() for r in repositories]).rename(columns={"id": "repository_id", "team": "team"})

        df_commits["repository_id"] = df_commits["repository"].apply(lambda x: x.id) # type: ignore

        df_commits = df_commits.merge( # type: ignore
            df_repos[["repository_id", "team"]], # type: ignore
            how="left",
            on="repository_id"
        )

        df_commits["total"] = df_commits["added_lines"] + df_commits["removed_lines"]

        result = df_commits.groupby(group_by)["total"].sum().reset_index(name="gross_productivity") # type: ignore
        
        return result



    @staticmethod
    def calculate_gross_use_of_AI_grouped_by(metrics: List[CopilotCodeMetrics], group_by: List[str]) -> pd.DataFrame:
        allowed = {"language", "team_id", "IDE", "copilot_model"}
        if not set(group_by).issubset(allowed):
            raise ValueError(f"Invalid group_by columns: {group_by}. Allowed: {allowed}")

        df: pd.DataFrame = pd.DataFrame([m.model_dump() for m in metrics])
        df["team_id"] = df["team"].apply(lambda t: t["id"] if t else None) # type: ignore

        result: pd.DataFrame = df.groupby(group_by)["lines_accepted"].sum().reset_index(name="gross_use_of_AI") # type: ignore
        return result


    @staticmethod
    def calculate_relative_use_of_AI_grouped_by(metrics: List[CopilotCodeMetrics], group_by: List[str]) -> pd.DataFrame:
        allowed = {"language", "team_id", "IDE", "copilot_model"}
        if not set(group_by).issubset(allowed):
            raise ValueError(f"Invalid group_by columns: {group_by}. Allowed: {allowed}")

        df: pd.DataFrame = pd.DataFrame([m.model_dump() for m in metrics])

        df["team_id"] = df["team"].apply(lambda t: t["id"] if t else None) # type: ignore

        grouped: pd.DataFrame = df.groupby(group_by).agg({ # type: ignore
            "lines_accepted": "sum",
            "lines_suggested": "sum"
        }).reset_index()

        grouped["relative_use_of_AI"] = grouped.apply( # type: ignore
            lambda row: row["lines_accepted"] / row["lines_suggested"] if row["lines_suggested"] > 0 else 0, # type: ignore
            axis=1
        )

        return grouped[group_by + ["relative_use_of_AI"]]  # type: ignore