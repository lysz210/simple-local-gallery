from fastapi import APIRouter
from ..dto import PhotoSummary
from ...storage.main import photos_summary

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("/", name="Get Photos summary")
async def get_photos_summary() -> list[PhotoSummary]:
    summaries = photos_summary()
    return [PhotoSummary.model_validate(item._mapping) for item in summaries]