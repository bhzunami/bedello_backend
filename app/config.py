from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseSettings, PostgresDsn, validator


class DatabaseUri(AnyUrl):
    allowed_schemes = {"postgres", "postgresql", "sqlite"}


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    ORIGINS: List[str] = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]

    # Do not read the environ variables -> do read a .env file
    class Config:
        #    case_sensitive = True
        env_file = ".env"


settings = Settings()
