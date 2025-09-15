import json
from pathlib import Path
from typing import Optional
from sqlalchemy.sql import (
    func
)

from sqlalchemy import JSON, create_engine, type_coerce
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

def search_photos(filter: dto.FilterPhotos) -> list[dto.Photo]:
    gallery_root = settings.GALLERY_ROOT
    folder = filter.folder
    if isinstance(folder, str):
        folder = Path(folder)
    
    with get_session() as s:
        query = s.query(models.Photo)
        if folder:
            if folder.is_absolute():
                folder = folder.relative_to(gallery_root)
            query = query.filter(models.Photo.folder == str(folder))
        photos = query.all()
        return [
            dto.Photo.model_validate(
                photo,
                from_attributes=True,
                strict=False
            )
            for photo in photos
        ]
def find_photo_by_id(id: int) -> Optional[dto.Photo]:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == id).first()
        return dto.Photo.model_validate(
            photo,
            from_attributes=True,
            strict=False
        ) if photo else None

def save_photos(photos_paths: list[Path]) -> dict[str, int]:
    photos = [models.Photo(
        folder=photo_path.parent.as_posix(),
        filename=photo_path.name,
        description=photo_path.name,
        original_created_at=func.datetime('now') # Placeholder, should extract from EXIF
    ) for photo_path in photos_paths]
    with get_session() as s:
        s.add_all(photos)
        s.commit()
        return {
            f"{photo.folder}/{photo.filename}": photo.id
            for photo in s.query(models.Photo)
               .where(func.concat(models.Photo.folder, '/', models.Photo.filename).in_(
                   [p.as_posix() for p in photos_paths]
               )) 
        }

def  tracks_summary() -> list[dto.TrackSummary]:
    with get_session() as s:
        results = s.query(
            models.GpsTrack.uid,
            models.GpsTrack.name,
            func.count(models.GpsPoint.id).label('total_points'),
            func.json_object(
                'min', func.json_object(
                    'latitude', func.min(models.GpsPoint.latitude),
                    'longitude', func.min(models.GpsPoint.longitude),
                    'elevation', func.min(models.GpsPoint.elevation),
                    'timestamp', func.min(models.GpsPoint.timestamp),
                ),
                'max', func.json_object(
                    'latitude', func.max(models.GpsPoint.latitude),
                    'longitude', func.max(models.GpsPoint.longitude),
                    'elevation', func.max(models.GpsPoint.elevation),
                    'timestamp', func.max(models.GpsPoint.timestamp),
                ),
            ).label('bounds')
        ).join(
            models.GpsPoint, models.GpsTrack.uid == models.GpsPoint.track_uid
        ).group_by(
            models.GpsTrack.uid
        ).all()

        summaries = []
        for item in results:
            mapping = dict(item._mapping)
            if mapping['bounds']:
                mapping['bounds'] = json.loads(mapping['bounds'])
            summaries.append(dto.TrackSummary.model_validate(mapping))
        return summaries

def save_track(track: dto.Track) -> None:
    new_track = models.GpsTrack(
        **track.model_dump(exclude=('bounds', 'points')),
        points=[models.GpsPoint(**point.model_dump()) for point in track.points] if track.points else None
    )
    with get_session() as s:
        s.add(new_track)
        s.commit()
        return new_track.uid