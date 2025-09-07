from datetime import timezone
from pathlib import Path
import gpxpy
from gpxpy.gpx import GPXTrackPoint
import pandas as pd

from ..api.dto import Bounds, Point, Track


def from_gpx_point(other: GPXTrackPoint) -> 'Point':
    return Point(
        timestamp=other.time.astimezone(timezone.utc),
        latitude=other.latitude,
        longitude=other.longitude,
        elevation=other.elevation
    )

def inspect_gpx(gpx_file: Path) -> Track:
    with gpx_file.open('r') as gpx_file:
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