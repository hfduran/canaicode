from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore

from src.cmd.dependencies.dependency_setters import set_fetch_copilot_metrics_dependencies
from src.infrastructure.database.connection.database_connection import SessionLocal # type: ignore

scheduler = BlockingScheduler()



@scheduler.scheduled_job('interval', days=1) # type: ignore
def fetch_metrics_job() -> None:
    print("Starting daily GitHub Copilot metrics collection")
    db = SessionLocal()

    fetch_copilot_metrics_use_case = set_fetch_copilot_metrics_dependencies(db)

    try:
        fetch_copilot_metrics_use_case.execute()
        print("Daily metrics collection completed successfully")

    except Exception as e:
        print(f"Error during daily metrics collection: {e}")

    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    print("Scheduler started. Waiting for next daily execution")
    scheduler.start() # type: ignore
