from datetime import datetime
from pathlib import Path
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