from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]
contracts_collection = database["contracts"]

def check_database_connection():
  try:
    client.admin.command("ping")
    return True
  except Exception:
    return False