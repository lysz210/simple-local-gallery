from fastapi import APIRouter
from ...storage.main import photos_summary
from ...api.dto import PhotoSummary

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("", name="Get Photos summary", operation_id="get_photos_summary")
async def get_photos_summary() -> list[PhotoSummary]:
    summaries = photos_summary()
    return [PhotoSummary.model_validate(item._mapping) for item in summaries]
