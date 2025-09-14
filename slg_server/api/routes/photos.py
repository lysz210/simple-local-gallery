from pathlib import Path
from fastapi import APIRouter

from ...storage.main import photos_summary, save_photos
from ...api.dto import PhotoSummary

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("", name="Get Photos summary", operation_id="get_photos_summary")
async def get_photos_summary() -> list[PhotoSummary]:
    summaries = photos_summary()
    return [PhotoSummary.model_validate(item._mapping) for item in summaries]

@router.post("/import", name="Import Photos", operation_id="import_photos")
async def import_pphotos(photos: list[Path]) -> dict[str, int]:
    return save_photos(photos)
