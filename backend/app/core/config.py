from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    s3_endpoint: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_bucket: str | None = None
    alert_webhook_url: str | None = None
    redis_url: str | None = None

    class Config:
        env_file = "./backend/.env.example"

settings = Settings()
