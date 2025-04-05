from pydantic import BaseModel
from typing import Callable
import typer

from datetime import datetime

from services.gh_copilot_services import GhCopilotServices
from services.git_repo_services import GitRepoServices

app = typer.Typer()


class Feature(BaseModel):
    title: str
    func: Callable


available_features: list[Feature] = [
    Feature(
        title="Summarize git",
        func=lambda: GitRepoServices.summarize_loc(
            start_date=datetime(2024, 1, 1),
            end_date=datetime.now(),
        ),
    ),
    Feature(
        title="Get GitHub Copilot metrics", func=GhCopilotServices.summarize_metrics
    ),
]


@app.command()
def main() -> None:
    number_of_functions: int = len(available_features)

    typer.echo("WELCOME TO CANAICODE!")

    while True:
        typer.echo("0. Exit")
        index: int = 0
        for feature in available_features:
            typer.echo(f"{index + 1}. {feature.title}")
            index += 1

        option_prompt = typer.prompt("")
        try:
            option: int = int(option_prompt)
        except Exception:
            typer.echo("Invalid selection!")
            continue

        if option == 0:
            typer.echo("Bye!! ><")
            return
        if option > number_of_functions:
            typer.echo("Invalid selection!")
            continue
        feature = available_features[option - 1]
        feature.func()


if __name__ == "__main__":
    app()
