import typer

from datetime import datetime

from services.gh_copilot_services import GhCopilotServices
from services.git_repo_services import GitRepoServices

app = typer.Typer()


@app.command()
def main() -> None:
    option = typer.prompt(
        "Please select a function:\n 1: summarize git\n 2: gh copilot\n", type=int
    )

    if option == 1:
        GitRepoServices.summarize_loc(
            start_date=datetime(2024, 1, 1),
            end_date=datetime.now(),
        )
    elif option == 2:
        GhCopilotServices.summarize_metrics()
    else:
        print("Invalid option!")


if __name__ == "__main__":
    app()
