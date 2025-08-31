from fastapi import APIRouter

from ..dto import PhotoSummary

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("/", name="Get Photos summary")
async def get_photos_summary() -> list[PhotoSummary]:
    return [PhotoSummary(path="/photos", total_photos=100, first_taken_at="2023-01-01T00:00:00", last_taken_at="2023-12-31T23:59:59")]