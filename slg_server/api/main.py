from fastapi import APIRouter

from .routes import photos, tracks, settings

api_router = APIRouter()
api_router.include_router(photos.router)
api_router.include_router(settings.router)
api_router.include_router(tracks.router)