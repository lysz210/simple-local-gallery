from datetime import timezone
from pathlib import Path
from fastapi import APIRouter
import gpxpy
from gpxpy.gpx import GPXTrackPoint
from ...core.config import settings

from ..dto import Point, Track, TrackSummary

from ...storage.main import tracks_summary

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("", name="Get Tracks summary", operation_id="get_tracks_summary")
async def get_tracks_summary() -> list[TrackSummary]:
    summaries = tracks_summary()
    return [
        TrackSummary.model_validate(item._mapping)
        for item in summaries
    ]

def from_gpx_point(other: GPXTrackPoint) -> 'Point':
    return Point(
        timestamp=other.time.astimezone(timezone.utc),
        latitude=other.latitude,
        longitude=other.longitude,
        elevation=other.elevation
    )
@router.get("/inspect/{gpx_file:path}", name="Inspect gpx file", operation_id="inspect_pgx_file")
async def inspec_pgx(gpx_file: str) -> Track:
    file_path = settings.GALLERY_ROOT / gpx_file

    with file_path.open('r') as gpx_file:
        doc = gpxpy.parse(gpx_file)
        track_uid = doc.link.rsplit('-', 1)[-1]
    
    points: list[Point] = [
        from_gpx_point(gpx_point)
        for point in doc.tracks
            for segment in point.segments
                for gpx_point in segment.points
    ]

    return Track(
        uid=track_uid,
        name=doc.name,
        timestamp=doc.time.astimezone(timezone.utc),
        points=points
    )