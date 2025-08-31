from pathlib import Path
from typing import Optional
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.sql import (
    func
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

class Base(DeclarativeBase):
    pass

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column()
    filename: Mapped[str] = mapped_column(unique=True, sqlite_on_conflict_unique="IGNORE")
    description: Mapped[str] = mapped_column()
    original_created_at: Mapped[datetime] = mapped_column()

    gps_point_id: Mapped[Optional[int]] = mapped_column(ForeignKey("points.id"))
    gps_point: Mapped[Optional["GpsPoint"]] = relationship(back_populates="photos")

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "filename": self.filename,
            "description": self.description,
            "original_created_at": self.original_created_at.isoformat(),
            "gps_point_id": self.gps_point_id,
        }

class GpsTrack(Base):
    __tablename__ = "tracks"

    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.datetime('now'))

    points: Mapped[Optional[list["GpsPoint"]]] = relationship(back_populates="track")

class GpsPoint(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    elevation: Mapped[Optional[float]] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.datetime('now'))

    track_uid: Mapped[Optional[str]] = mapped_column(ForeignKey("tracks.uid"))
    track: Mapped[Optional["GpsTrack"]] = relationship(back_populates="points")

    photos: Mapped[Optional[list["Photo"]]] = relationship(back_populates="gps_point")
    
    __table_args__ = (
        UniqueConstraint('track_uid', 'timestamp', name='_gps_unique_track_point'),
    )

def get_session():

    engine = create_engine(settings.sqlite_dsn, echo=True)
    SessionLocal = sessionmaker(autoflush=True, bind=engine)
    return SessionLocal()

def photos_summary():
    with get_session() as s:
        return s.query(
            Photo.path,
            func.count(Photo.id).label('total_photos'),
            func.min(Photo.original_created_at).label('first_taken_at'),
            func.max(Photo.original_created_at).label('last_taken_at'),
        ).group_by(Photo.path).all()

def get_photos_in_folder(folder: Path) -> list[Photo]:
    gallery_root = settings.gallery_root
    if isinstance(folder, str):
        folder = Path(folder)
    
    if folder.is_absolute():
        folder = folder.relative_to(gallery_root)
    with get_session() as s:
        return s.query(Photo).filter(Photo.path == str(folder)).all()