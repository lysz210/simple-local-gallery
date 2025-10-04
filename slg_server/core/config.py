from pathlib import Path
import secrets
from tkinter.filedialog import askdirectory
from urllib.parse import urljoin
import warnings
from typing import Annotated, Any, Literal, Optional

import httpx
from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    SecretStr,
    computed_field,
    model_validator
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from typing_extensions import Self

from google.genai import Client

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
        # Use top level .env file
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: SecretStr = secrets.token_urlsafe(32)
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
    FIRST_SUPERUSER_PASSWORD: SecretStr

    def _check_default_secret(self, var_name: str, value: SecretStr | None) -> None:
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
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def thumbnails_root(self) -> Path:
        thumb_root = self.GALLERY_ROOT / ".thumbnails"
        thumb_root.mkdir(exist_ok=True)
        return thumb_root

    GEMINI_API_KEY: Optional[SecretStr] = None

    @computed_field
    @property
    def gemini(self) -> Client:
        if self.GEMINI_API_KEY is None:
            raise RuntimeError("GEMINI_API_KEY is not set in the configuration.")
        return Client(
            api_key=self.GEMINI_API_KEY.get_secret_value(),
        )

settings = Settings()  # type: ignore

class FlickrSettings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file
        env_file=".env",
        env_ignore_empty=True,
        env_prefix='FLICKR_',
        extra="ignore",
    )

    API_KEY: SecretStr
    SECRET:  SecretStr
    OAUTH_BASE_URL: HttpUrl
    SERVICE_BASE_URL: HttpUrl

    @computed_field
    @property
    def request_token_url(self) -> str:
        return urljoin(self.OAUTH_BASE_URL.unicode_string(), 'request_token')

    @computed_field
    @property
    def authorization_url(self) -> str:
        return urljoin(self.OAUTH_BASE_URL.unicode_string(), 'authorize')
    
    @computed_field
    @property
    def access_token_url(self) -> str:
        return urljoin(self.OAUTH_BASE_URL.unicode_string(), 'access_token')

class OsmNominatimSettings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use topo level .env file
        env_file=".env",
        env_ignore_empty=True,
        env_prefix='OSM_NOMINATIM_',
        extra='ignore'
    )

    SERVICE_BASE_URL: HttpUrl
    LANG: str
    ZOOM: int

    @computed_field
    @property
    def http_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.SERVICE_BASE_URL.unicode_string(),
            headers={'Accept-Language': self.LANG},
            params={'format': 'json', 'zoom': self.ZOOM}
        )