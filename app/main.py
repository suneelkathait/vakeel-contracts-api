from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.contracts import router as contracts_router
from app.database.mongodb import check_database_connection

app = FastAPI(
  title=settings.APP_NAME,
  version=settings.APP_VERSION,
  description="AI-powered contract analysis API",
)

@app.get("/")
def root():
  return {
    "message": "Vakeel Contracts API is running",
    "environment": settings.ENVIRONMENT,
    "database_connected": check_database_connection(),
  }

app.include_router(contracts_router)