from app.database.mongodb import check_database_connection
from app.exceptions.application import AppException

def ensure_database_connection():
  is_connected = check_database_connection()

  if not is_connected:
    raise AppException(
      message="Database is currently unavailable. Please try again later.",
      status_code=503,
      error_code="DATABASE_CONNECTION_ERROR",
    )