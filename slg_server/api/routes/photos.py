from pathlib import Path
from typing import Optional
from typing import Annotated
from fastapi import APIRouter, Query

from ...storage import main as storage
from ...api import dto

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("", name="Get Photos summary", operation_id="get_photos_summary")
async def get_photos_summary() -> list[dto.PhotoSummary]:
    summaries = storage.photos_summary()
    return [dto.PhotoSummary.model_validate(item._mapping) for item in summaries]

@router.get("/search", name="Search photos", operation_id="search_photos")
async def get_photos_in_folder(filter: Annotated[dto.FilterPhotos, Query()]) -> list[dto.Photo]:
    return storage.search_photos(filter)

@router.get("/{id:int}", name="Get Photo by ID", operation_id="get_photo_by_id")
async def get_photo_by_id(id: int) -> Optional[dto.Photo]:
    return storage.find_photo_by_id(id)

@router.put("/{id:int}/point", name="Update Photo Point", operation_id="update_photo_point")
async def update_photo_point(id: int, point: dto.PointWithTrackUid) -> Optional[dto.Photo]:
    return storage.update_photo_point(id, point)

@router.post("/import", name="Import Photos", operation_id="import_photos")
async def import_pphotos(photos: list[Path]) -> dict[str, int]:
    return storage.save_photos(photos)
