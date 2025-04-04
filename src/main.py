from datetime import datetime

from services.summarize_service import SummaryService

def main() -> None:
    SummaryService.summarize_git_loc(
        start_date=datetime(2024, 1, 1),
        end_date=datetime.now(),
    )


if __name__ == "__main__":
    main()
