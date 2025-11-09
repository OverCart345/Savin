import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

# Load .env from users_service directory (not src)
users_service_root = Path(__file__).parent.parent.parent
env_file = users_service_root / ".env"
load_dotenv(dotenv_path=env_file)

class Settings(BaseModel):
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "users_db")
    postgres_user: str = os.getenv("POSTGRES_USER", "app")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "app")

    secret_key: str = os.getenv("SECRET_KEY", "change_me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
