import typer

from datetime import datetime

from consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from services.summarize_service import SummaryService

app = typer.Typer()


@app.command()
def main() -> None:
    option = typer.prompt(
        "Please select a function:\n 1: summarize git\n 2: gh copilot\n", type=int
    )

    if option == 1:
        SummaryService.summarize_git_loc(
            start_date=datetime(2024, 1, 1),
            end_date=datetime.now(),
        )
    elif option == 2:
        GhCopilotConsumer().getMetrics()
    else:
        print("Invalid option!")


if __name__ == "__main__":
    app()
