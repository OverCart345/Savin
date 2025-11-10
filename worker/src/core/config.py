import os
from pathlib import Path

from dotenv import load_dotenv

worker_root = Path(__file__).parent.parent.parent
env_file = worker_root / ".env"
load_dotenv(dotenv_path=env_file)


class Settings:
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "users_db")
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    push_url: str = os.getenv("PUSH_URL", "http://push-notificator:8000/notify")

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
