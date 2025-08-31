from fastapi import APIRouter

from .routes import photos, settings

api_router = APIRouter()
api_router.include_router(photos.router)
api_router.include_router(settings.router)