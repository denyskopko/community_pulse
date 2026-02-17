from pathlib import Path
from typing import Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# BASE_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # project info
    app_name: str
    debug: bool = False

    # DB settings
    mysql_host: SecretStr
    mysql_port: int
    mysql_user: str
    mysql_password: SecretStr
    mysql_database: str
    mysql_pool_size: int
    mysql_pool_timeout: int

    # API settings
    api_prefix: str
    api_version: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    @property
    def database_url(self):
        url = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

        return url.format(
            user=self.mysql_user,
            password=self.mysql_password.get_secret_value(),
            host=self.mysql_host.get_secret_value(),
            port=self.mysql_port,
            db_name=self.mysql_database
        )

    def get_flask_config(self) -> dict[str, Any]:
        return {
            "DEBUG": self.debug,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_POOL_SIZE": self.mysql_pool_size,
            "SQLALCHEMY_POOL_TIMEOUT": self.mysql_pool_timeout,
        }


settings = Settings()
