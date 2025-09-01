from fastapi import APIRouter

from .routes import (
    photos,
    settings,
    tracks,
    filesystem
)

api_router = APIRouter()
api_router.include_router(photos.router)
api_router.include_router(settings.router)
api_router.include_router(tracks.router)
api_router.include_router(filesystem.router)