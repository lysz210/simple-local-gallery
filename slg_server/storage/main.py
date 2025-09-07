from pathlib import Path
from sqlalchemy.sql import (
    func
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

from . import models
from ..api import dto

def get_session():

    engine = create_engine(settings.sqlite_dsn, echo=True)
    SessionLocal = sessionmaker(autoflush=True, bind=engine)
    return SessionLocal()

def photos_summary():
    with get_session() as s:
        return s.query(
            models.Photo.folder,
            func.count(models.Photo.id).label('total_photos'),
            func.min(models.Photo.original_created_at).label('first_taken_at'),
            func.max(models.Photo.original_created_at).label('last_taken_at'),
        ).group_by(models.Photo.folder).all()

def get_photos_in_folder(folder: Path) -> list[models.Photo]:
    gallery_root = settings.GALLERY_ROOT
    if isinstance(folder, str):
        folder = Path(folder)
    
    if folder.is_absolute():
        folder = folder.relative_to(gallery_root)
    with get_session() as s:
        return s.query(models.Photo).filter(models.Photo.folder == str(folder)).all()

def  tracks_summary():
    with get_session() as s:
        return s.query(
            models.GpsTrack.uid,
            models.GpsTrack.name,
            func.count(models.GpsPoint.id).label('total_points'),
            func.min(models.GpsPoint.timestamp).label('start_time'),
            func.max(models.GpsPoint.timestamp).label('finish_time'),
        ).join(
            models.GpsPoint, models.GpsTrack.uid == models.GpsPoint.track_uid
        ).group_by(
            models.GpsTrack.uid
        ).all()

def save_track(track: dto.Track) -> None:
    new_track = models.GpsTrack(
        **track.model_dump(exclude=('bounds', 'points')),
        points=[models.GpsPoint(**point.model_dump()) for point in track.points] if track.points else None
    )
    with get_session() as s:
        s.add(new_track)
        s.commit()
        return new_track.uid