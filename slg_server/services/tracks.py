from datetime import timezone
from pathlib import Path
import gpxpy
from gpxpy.gpx import GPXTrackPoint
import pandas as pd

from ..api import dto
from ..storage import main as storage
from ..core.config import OsmNominatimSettings
from .nominatim import NominatimService

nominatim_service = NominatimService(OsmNominatimSettings())

def from_gpx_point(other: GPXTrackPoint) -> dto.Point:
    return dto.Point(
        timestamp=other.time.astimezone(timezone.utc),
        latitude=other.latitude,
        longitude=other.longitude,
        elevation=other.elevation
    )

def inspect_gpx(gpx_file: Path, with_bounds: bool = True) -> dto.Track:
    with gpx_file.open('r') as gpx_file:
        doc = gpxpy.parse(gpx_file)
        track_uid = doc.link.rsplit('-', 1)[-1]
    
    points: list[dto.Point] = [
        from_gpx_point(gpx_point)
        for point in doc.tracks
            for segment in point.segments
                for gpx_point in segment.points
    ]

    track = dto.Track(
        uid=track_uid,
        name=doc.name,
        timestamp=doc.time.astimezone(timezone.utc),
        points=points,
    )

    if (with_bounds):
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
        track.bounds=dto.Bounds(
            min=dto.Point(
                latitude=min_max['latitude_min'],
                longitude=min_max['longitude_min'],
                elevation=min_max['elevation_min'],
                timestamp=min_max['timestamp_min']
            ),
            max=dto.Point(

                latitude=min_max['latitude_max'],
                longitude=min_max['longitude_max'],
                elevation=min_max['elevation_max'],
                timestamp=min_max['timestamp_max']
            ),
        )
    
    return track

async def locate_photo_on_track(photo_id: int) -> list[dto.PointWithTrackUid]:
    points = storage.locate_photo_on_track(photo_id)
    for point in points:
        if (point.address):
            continue

        point.address = nominatim_service.reverse(point.latitude, point.longitude)
    return points
