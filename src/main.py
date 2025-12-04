from fastapi.openapi.utils import get_openapi
from src.infrastructure.logger.logger_config import logger
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.cmd.api.routes import router
from src.cmd.scheduler.scheduler import start_scheduler
from src.infrastructure.database.init_db import init_database


@asynccontextmanager # type: ignore
async def lifespan(app: FastAPI) -> Any:
    """Handle application lifespan events"""
    # Startup
    try:
        logger.info("Initializing database...")
        init_database()
        logger.info("Database initialization completed successfully!")
        start_scheduler()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # You might want to raise the exception to prevent the app from starting
        # with an uninitialized database
        raise
    
    yield
    
    # Shutdown (cleanup code can go here if needed)
    logger.info("Application shutting down...")


app = FastAPI(lifespan=lifespan, root_path="/api")

# Configure CORS - Allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
        openapi_version="3.0.0"
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

