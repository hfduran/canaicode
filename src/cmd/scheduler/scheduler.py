from src.infrastructure.logger.logger_config import logger
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore

from src.cmd.dependencies.dependency_setters import set_fetch_copilot_metrics_dependencies
from src.infrastructure.database.connection.database_connection import SessionLocal # type: ignore



scheduler = BackgroundScheduler()

def start_scheduler() -> None:
    scheduler.start() # type: ignore


@scheduler.scheduled_job('interval', days=1) # type: ignore
def fetch_metrics_job() -> None:
    logger.info("Starting daily GitHub Copilot metrics collection")
    db = SessionLocal()

    fetch_copilot_metrics_use_case = set_fetch_copilot_metrics_dependencies(db)

    try:
        fetch_copilot_metrics_use_case.execute()
        logger.info("Daily metrics collection completed successfully")

    except Exception as e:
        logger.error(f"Error during daily metrics collection: {e}")

    finally:
        db.close()
        logger.info("Database session closed.")

if __name__ == "__main__":
    logger.info("Scheduler started. Waiting for next daily execution")
    start_scheduler()
