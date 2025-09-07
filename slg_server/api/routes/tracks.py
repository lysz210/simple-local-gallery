from datetime import timezone
from pathlib import Path
from fastapi import APIRouter
import gpxpy
from gpxpy.gpx import GPXTrackPoint
from ...core.config import settings

from ..dto import Bounds, Point, Track, TrackSummary

from ...storage.main import tracks_summary
import pandas as pd

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
@router.get("/inspect/{gpx_file:path}", name="Inspect gpx file", operation_id="inspect_gpx_file")
async def inspec_gpx(gpx_file: str) -> Track:
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

    pointsTable = pd.DataFrame([p.model_dump() for p in points])

    min_max = {
        'timestamp_min': pointsTable['timestamp'].min(),
        'timestamp_max': pointsTable['timestamp'].max(),
        'latitude_min': pointsTable['latitude'].min(),
        'latitude_max': pointsTable['latitude'].max(),
        'longitude_min': pointsTable['longitude'].min(),
        'longitude_max': pointsTable['longitude'].max(),
        'elevation_min': pointsTable['elevation'].min(),
        'elevation_max': pointsTable['elevation'].max(),
    }

    return Track(
        uid=track_uid,
        name=doc.name,
        timestamp=doc.time.astimezone(timezone.utc),
        points=points,
        bounds=Bounds(
            min=Point(
                latitude=min_max['latitude_min'],
                longitude=min_max['longitude_min'],
                elevation=min_max['elevation_min'],
                timestamp=min_max['timestamp_min']
            ),
            max=Point(

                latitude=min_max['latitude_max'],
                longitude=min_max['longitude_max'],
                elevation=min_max['elevation_max'],
                timestamp=min_max['timestamp_max']
            ),
        )
    )
