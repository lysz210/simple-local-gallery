from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from pydantic_core import Url

class Photo(BaseModel):
    id: int
    folder: str
    filename: str
    title: Optional[str] = None
    description: Optional[str]
    original_created_at: datetime
    tags: Optional[list[str]] = None
    point: Optional['PointWithTrackUid'] = None

class PhotoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    point_id: Optional[int] = None

class PhotoInfo(BaseModel):
    id: int
    title: str
    description: str
    tags: list[str]
    feedback: Optional[str]

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
    address: Optional['Address'] = None

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

class FlickrState(BaseModel):
    fullname: str
    user_nsid: str
    username: str

class FlickrResponse(BaseModel):
    state: Optional[FlickrState] = None
    redirect_uri: Optional[Url] = None

class Token(BaseModel):
    token: str = Field(alias="oauth_token")
    token_secret: str = Field(alias="oauth_token_secret")

class RequestToken(Token):
    callback_confirmed: bool = Field(alias='oauth_callback_confirmed')

class AccessToken(FlickrState, Token):
    pass

class FlickrPhotoInfo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    posted: Optional[datetime] = None
    taken: Optional[datetime] = None
    lastupdate: Optional[datetime] = None
    tags: Optional[list[str]] = None
    urls: Optional[list[HttpUrl]] = None

class Address(BaseModel):
    uid: UUID
    display_name: str
    country: str
    state: Optional[str] = None
    county: Optional[str] = None
    municipality: Optional[str] = None
    town: Optional[str] = None
    postcode: Optional[str] = None