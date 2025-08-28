from datetime import datetime, timezone
from pydantic import BaseModel
from gpxpy.gpx import GPXTrackPoint

class Point(BaseModel):
    time: datetime
    latitude: float
    longitude: float
    elevation: float | None
    type: str
    color: str
    name: str | None

def from_gpx_point(other: GPXTrackPoint) -> 'Point':
    return Point(
        time=other.time.astimezone(timezone.utc),
        latitude=other.latitude,
        longitude=other.longitude,
        elevation=other.elevation,
        type='point',
        color='#00ff00',
        name=None
    )
