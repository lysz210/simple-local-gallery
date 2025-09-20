from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

class Photo(BaseModel):
    id: int
    folder: str
    filename: str
    description: str
    original_created_at: datetime
    point: Optional['PointWithTrackUid'] = None

class PhotoInfo(BaseModel):
    id: int
    description: str
    tags: list[str]

class PhotoSummary(BaseModel):
    folder: str
    total_photos: int
    first_taken_at: datetime
    last_taken_at: datetime

class FolderSummary(BaseModel):
    folder: Path
    total_photos: int

class FileSystemSummary(BaseModel):
    folders: list[FolderSummary]
    gpx_files_count: int

class Point(BaseModel):
    id: Optional[int] = None
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    timestamp: datetime

class PointWithTrackUid(Point):
    track_uid: str

class Bounds(BaseModel):
    min: Point
    max: Point

class Track(BaseModel):
    uid: str
    name: str
    description: Optional[str] = None
    bounds: Optional[Bounds] = None
    timestamp: Optional[datetime] = None
    points: Optional[list[Point]] = None

class TrackSummary(BaseModel):
    uid: str
    name: str
    total_points: int
    bounds: Optional[Bounds] = None

class FilterPhotos(BaseModel):
    folder: Optional[Path] = None