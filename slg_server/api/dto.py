from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

class Photo(BaseModel):
    id: int
    folder: str
    filename: str
    description: str
    original_created_at: str
    gps_point_id: int | None

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
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    timestamp: datetime

class Track(BaseModel):
    uid: str
    name: str
    description: Optional[str] = None
    timestamp: Optional[datetime] = None
    points: Optional[list[Point]] = None

class TrackSummary(BaseModel):
    uid: str
    name: str
    total_points: int
    start_time: datetime
    finish_time: datetime