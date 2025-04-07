from pydantic import BaseModel
from typing import Any, Callable
import typer

from datetime import datetime, date, timedelta

from services.gh_copilot_services import GhCopilotServices
from services.git_repo_services import GitRepoServices

app = typer.Typer()


class Feature(BaseModel):
    title: str
    func: Callable[[], Any]


def prompt_date(variable_name: str, default: date | None = None) -> date:
    while True:
        if default is None:
            date_str = typer.prompt(
                f"Enter {variable_name} (YYYY-MM-DD)",
            )
        else:
            date_str = typer.prompt(
                f"Enter {variable_name} (YYYY-MM-DD)",
                default=default.strftime("%Y-%m-%d"),
            )
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            typer.secho("Invalid format. Try again.", fg=typer.colors.RED)


def get_old_date() -> date:
    return datetime.today().date() - timedelta(days=365)


def get_tomorrow() -> date:
    return datetime.today().date() + timedelta(days=1)


available_features: list[Feature] = [
    Feature(
        title="Summarize git LoC by author",
        func=lambda: GitRepoServices.summarize_loc_by_author(
            start_date=prompt_date("start date", get_old_date()),
            end_date=prompt_date("end date", get_tomorrow()),
        ),
    ),
    Feature(
        title="Summarize git LoC by programming language",
        func=lambda: GitRepoServices.summarize_loc_by_language(
            start_date=prompt_date("start date", get_old_date()),
            end_date=prompt_date("end date", get_tomorrow()),
        ),
    ),
    Feature(
        title="Get GitHub Copilot metrics",
        func=lambda: GhCopilotServices.summarize_metrics(
            start_date=prompt_date("start date", get_old_date()),
            end_date=prompt_date("end date", get_tomorrow()),
        ),
    ),
]


@app.command()
def main() -> None:
    number_of_functions: int = len(available_features)

    __print_welcome()

    while True:
        typer.echo("\nPlease select an option from the list below:")
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


def __print_welcome() -> None:
    with open("./assets/art.txt", "r") as file:
        content = file.read()
        typer.echo(content)
    with open("./assets/title.txt", "r") as file:
        content = file.read()
        typer.echo(content)


if __name__ == "__main__":
    app()
