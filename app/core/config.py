from pydantic_settings import BaseSettings, SettingsConfigDict

# Load configuration values from environment variables or .env.
class Settings(BaseSettings):
  APP_NAME: str = "Vakeel Contracts API"
  APP_VERSION: str = "1.0.0"
  ENVIRONMENT: str = "development"

  GEMINI_API_KEY: str

  MONGODB_URL: str
  DATABASE_NAME: str

  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore"
  )

settings = Settings()