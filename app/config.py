from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel


class CORSSettings(BaseModel):
    allow_origins: list["str"] = ["*"]
    allow_credentials: bool = True
    allow_methods: list["str"] = ["*"]
    allow_headers: list["str"] = ["*"]


class Settings(BaseSettings):
    project_name: str = "My Project"

    database_url: str = "sqlite+aiosqlite:///./sql_app.db"
    database_echo: bool = True
    database_connection_args: dict = (
        {"check_same_thread": False} if "sqlite" in database_url else {}
    )

    access_token_expire_minutes: int = 15

    secret_key: str = Field(default=...)
    algorithm: str = Field(default=...)

    smtp_host: str = Field(default=...)
    smtp_port: int = Field(default=...)
    email_address: str = Field(default=...)
    email_password: str = Field(default=...)

    cors_settings: CORSSettings = CORSSettings()

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"), case_sensitive=False
    )


settings = Settings()
