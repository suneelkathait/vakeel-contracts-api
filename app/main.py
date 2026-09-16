from fastapi import FastAPI
from app.core.config import settings
from app.exceptions.application import AppException
from app.exceptions.handlers import app_exception_handler
from app.api.routes.contracts import router as contracts_router
from app.database.mongodb import check_database_connection
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(
  title=settings.APP_NAME,
  version=settings.APP_VERSION,
  description="AI-powered contract analysis API",
)

app.add_exception_handler(
  AppException,
  app_exception_handler,
)

@app.get("/")
def root():
  return {
    "message": "Vakeel Contracts API is running",
    "environment": settings.ENVIRONMENT,
    "database_connected": check_database_connection(),
  }

app.include_router(contracts_router)