from src.infrastructure.logger.logger_config import logger
from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore

from src.cmd.dependencies.dependency_setters import set_fetch_copilot_metrics_dependencies, set_send_metrics_email_dependencies
from src.infrastructure.database.connection.database_connection import SessionLocal # type: ignore



scheduler = BlockingScheduler()

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


@scheduler.scheduled_job('interval', seconds=1) # type: ignore
def send_email_job() -> None:
    logger.info("Starting weekly metrics email dispatch")
    db = SessionLocal()

    send_metrics_email_use_case = set_send_metrics_email_dependencies(db)

    try:
        send_metrics_email_use_case.execute()
        logger.info("Weekly metrics email dispatch completed successfully")

    except Exception as e:
        logger.error(f"Error during weekly metrics email dispatch: {e}")

    finally:
        db.close()
        logger.info("Database session closed.")
        scheduler.shutdown() # type: ignore


if __name__ == "__main__":
    logger.info("Scheduler started. Waiting for next daily execution")
    start_scheduler()
