from datetime import datetime
from pydantic import BaseModel

class Photo(BaseModel):
    id: int
    path: str
    filename: str
    description: str
    original_created_at: str
    gps_point_id: int | None

class PhotoSummary(BaseModel):
    path: str
    total_photos: int
    first_taken_at: datetime
    last_taken_at: datetime