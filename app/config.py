from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel, computed_field


class CORSSettings(BaseModel):
    allow_origins: list["str"] = ["*"]
    allow_credentials: bool = True
    allow_methods: list["str"] = ["*"]
    allow_headers: list["str"] = ["*"]


class SMTPSettings(BaseModel):
    smtp_connection: Literal["SSL", "TLS"] = "TLS"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587 if smtp_connection == "TLS" else 465


class Settings(BaseSettings):
    project_name: str = "My Project"
    test_mode: bool = False

    database_host: str = Field(default=...)
    database_port: str = Field(default=...)
    database_user: str = Field(default=...)
    database_password: str = Field(default=...)
    database_db: str = Field(default=...)
    database_name: str = "postgresql"
    database_driver: str = "asyncpg"

    @property
    def database_url(self) -> str:
        return (
            (
                f"{self.database_name}+{self.database_driver}://"
                f"{self.database_user}:{self.database_password}@"
                f"{self.database_host}:{self.database_port}/{self.database_db}"
            )
            if not self.test_mode
            else "sqlite+aiosqlite:///:memory:"
        )

    database_echo: bool = True
    database_connection_args: dict = (
        {"check_same_thread": False} if "sqlite" in database_name else {}
    )

    access_token_expire_minutes: int = 15
    activation_token_expire_minutes: int = 60 * 24

    secret_key: str = Field(default=...)
    algorithm: str = Field(default=...)

    smtp_settings: SMTPSettings = SMTPSettings()
    email_address: str = Field(default=...)
    email_password: str = Field(default=...)

    cors_settings: CORSSettings = CORSSettings()

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"), case_sensitive=False
    )


settings = Settings()
