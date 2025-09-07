from fastapi import APIRouter, HTTPException

from ...services import tracks as tracks_service
from ...core.config import settings
from ..dto import Track, TrackSummary
from ...storage.main import tracks_summary

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("", name="Get Tracks summary", operation_id="get_tracks_summary")
async def get_tracks_summary() -> list[TrackSummary]:
    summaries = tracks_summary()
    return [
        TrackSummary.model_validate(item._mapping)
        for item in summaries
    ]


@router.get("/inspect/{gpx_file:path}", name="Inspect gpx file", operation_id="inspect_gpx_file")
async def inspec_gpx(gpx_file: str) -> Track:
    file_path = settings.GALLERY_ROOT / gpx_file

    if not file_path.exists():
        raise HTTPException(status_code=404)

    return tracks_service.inspect_gpx(file_path)