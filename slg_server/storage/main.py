from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo
import piexif
from sqlalchemy.sql import (
    func
)
from PIL import Image

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

def to_photo_dto(photo: models.Photo) -> dto.Photo:
    photo_dto = dto.Photo.model_validate(
        photo,
        from_attributes=True,
        strict=False
    )
    if photo.gps_point:
        photo_dto.point = dto.PointWithTrackUid.model_validate(
            photo.gps_point,
            from_attributes=True,
            strict=False
        )
    return photo_dto

def update_photo(id: int, photo_patch: dto.PhotoPatch) -> dto.Photo:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == id).first()
        for key, value in photo_patch.model_dump(exclude_unset=True).items():
            if key == 'point_id':
                photo.gps_point_id = value
            else:
                setattr(photo, key, value)
        s.commit()
        return to_photo_dto(photo)

def get_photo_path(id: int) -> Path:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == id).first()
        return Path(photo.folder) / photo.filename

def get_photo_name(id: int) -> str:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == id).first()
        return Path(photo.filename).stem

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
            to_photo_dto(photo)
            for photo in photos
        ]
def find_photo_by_id(id: int) -> Optional[dto.Photo]:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == id).first()
        return to_photo_dto(photo) if photo else None

def save_photos(photos_paths: list[Path]) -> dict[str, int]:
    europe_rome = ZoneInfo('Europe/Rome')
    gallery_root = settings.GALLERY_ROOT
    photos = []
    for photo_path in photos_paths:
        full_path = gallery_root / photo_path
        image = Image.open(full_path)
        exif = piexif.load(image.info["exif"])
        metas = exif["Exif"]
        created_at = metas.get(piexif.ExifIFD.DateTimeOriginal, None)
        created_offset = metas.get(piexif.ExifIFD.OffsetTimeOriginal, None)
        if created_offset:
            created_at_with_offset = created_at.decode() + created_offset.decode()
            original_datetime = ( datetime.strptime(created_at_with_offset, "%Y:%m:%d %H:%M:%S%z")
                                .astimezone(timezone.utc))
        elif created_at:
            original_datetime = (datetime
                                .strptime(created_at.decode(), "%Y:%m:%d %H:%M:%S")
                                .astimezone(europe_rome).astimezone(timezone.utc)
                            )
        else:
            original_datetime = datetime.now(timezone.utc)

        photos.append(models.Photo(
            folder=str(photo_path.parent),
            filename=photo_path.name,
            original_created_at=original_datetime
        ))
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

def update_photo_point(photo_id: int, point: dto.PointWithTrackUid) -> Optional[dto.Photo]:
    with get_session() as s:
        if not point.id:
            point_model = models.GpsPoint(**point.model_dump())
            s.add(point_model)
            s.commit()
            point.id = point_model.id

        photo_model = s.query(models.Photo).filter(models.Photo.id == photo_id).first()
        photo_model.gps_point_id = point.id
        s.commit()
        return to_photo_dto(photo_model)

def locate_photo_on_track(photo_id: int) -> list[dto.PointWithTrackUid]:
    with get_session() as s:
        photo = s.query(models.Photo).filter(models.Photo.id == photo_id).first()
        located_photo = dto.Photo.model_validate(photo, from_attributes=True, strict=False)
        if not photo or not photo.original_created_at:
            return located_photo
        photo_time = photo.original_created_at

        tracks_uid = s.query(models.GpsPoint.track_uid).group_by(models.GpsPoint.track_uid).having(
            func.max(models.GpsPoint.timestamp) >= photo_time,
            func.min(models.GpsPoint.timestamp) <= photo_time
        ).all()

        points: list[dto.PointWithTrackUid] = []

        for (track_uid,) in tracks_uid:
            before_point = s.query(models.GpsPoint).filter(
                models.GpsPoint.track_uid == track_uid,
                models.GpsPoint.timestamp <= photo_time
            ).order_by(models.GpsPoint.timestamp.desc()).first()
            after_point = s.query(models.GpsPoint).filter(
                models.GpsPoint.track_uid == track_uid,
                models.GpsPoint.timestamp >= photo_time
            ).order_by(models.GpsPoint.timestamp.asc()).first()
            
            point = dto.PointWithTrackUid(
                track_uid=track_uid,
                latitude= (before_point.latitude + after_point.latitude) / 2,
                longitude= (before_point.longitude + after_point.longitude) / 2,
                elevation= (before_point.elevation + after_point.elevation) / 2,
                timestamp=photo_time
            ) if before_point.id != after_point.id else dto.PointWithTrackUid.model_validate(before_point, from_attributes=True, strict=False)
            points.append(point)

        return points

def tracks_summary() -> list[dto.TrackSummary]:
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