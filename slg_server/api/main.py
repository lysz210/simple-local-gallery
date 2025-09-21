from fastapi import APIRouter

from .routes import (
    photos,
    settings,
    tracks,
    filesystem,
    ai,
    flickr
)

api_router = APIRouter()
api_router.include_router(photos.router)
api_router.include_router(settings.router)
api_router.include_router(tracks.router)
api_router.include_router(filesystem.router)
api_router.include_router(ai.router)
api_router.include_router(flickr.router, prefix="/socials")