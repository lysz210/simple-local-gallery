from fastapi import APIRouter, HTTPException

from ...services import tracks as tracks_service
from ...core.config import settings
from .. import dto
from ...storage import main as storage

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("", name="Get Tracks summary", operation_id="get_tracks_summary")
async def get_tracks_summary() -> list[dto.TrackSummary]:
    return storage.tracks_summary()

@router.get("/inspect/{gpx_file:path}", name="Inspect gpx file", operation_id="inspect_gpx_file")
async def inspec_gpx(gpx_file: str) -> dto.Track:
    file_path = settings.GALLERY_ROOT / gpx_file

    if not file_path.exists():
        raise HTTPException(status_code=404)

    return tracks_service.inspect_gpx(file_path)

@router.post("/import/{gpx_file:path}", name="Import gpx file into DB", operation_id="import_pgx_file")
async def import_gpx(gpx_file: str) -> str:
    file_path = settings.GALLERY_ROOT / gpx_file

    if not file_path.exists():
        raise HTTPException(status_code=404)

    return storage.save_track(tracks_service.inspect_gpx(file_path, with_bounds=False))

@router.get("/locate-photo", name="Locate Photo on Track", operation_id="locate_photo_on_track")
async def locate_photo_on_track(photo_id: int) -> list[dto.PointWithTrackUid]:
    return await tracks_service.locate_photo_on_track(photo_id)
