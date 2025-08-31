from fastapi import APIRouter

from .routes import photos

api_router = APIRouter()
api_router.include_router(photos.router)