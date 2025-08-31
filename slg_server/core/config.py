from pathlib import Path
import secrets
from tkinter.filedialog import askdirectory
import warnings
from typing import Annotated, Any, Literal, Optional

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    computed_field,
    model_validator
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from typing_extensions import Self

from ..storage import models

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

def ask_for_gallery_root() -> Path:
    selected = askdirectory(title="Select Gallery Root Directory")
    return Path(selected)

def init_gallery_root(root: Path) -> None:
    db_path = root / "photos.db"
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    models.Base.metadata.create_all(engine)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self
    
    GALLERY_ROOT: Optional[Path] = None
    @model_validator(mode="after")
    def _check_gallery_root(self) -> Self:
        if self.GALLERY_ROOT is None:
            self.GALLERY_ROOT = ask_for_gallery_root()
        init_gallery_root(self.GALLERY_ROOT)
        return self
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlite_dsn(self) -> Path:
        sqlite_path = self.GALLERY_ROOT / "photos.db"
        return f"sqlite:///{sqlite_path}"


settings = Settings()  # type: ignore