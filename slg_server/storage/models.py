from typing import Optional
from datetime import datetime
from sqlalchemy import (
    JSON,
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

class Base(DeclarativeBase):
    type_annotation_map = {
        list[str]: JSON
    }

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    folder: Mapped[str] = mapped_column()
    filename: Mapped[str] = mapped_column(unique=True, sqlite_on_conflict_unique="IGNORE")
    title: Mapped[Optional[str]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    original_created_at: Mapped[datetime] = mapped_column()
    tags: Mapped[Optional[list[str]]] = mapped_column()

    gps_point_id: Mapped[Optional[int]] = mapped_column(ForeignKey("points.id"))
    gps_point: Mapped[Optional["GpsPoint"]] = relationship(back_populates="photos")


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
    latitude: Mapped[float] = mapped_column(index=True)
    longitude: Mapped[float] = mapped_column(index=True)
    elevation: Mapped[Optional[float]] = mapped_column(index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.datetime('now'), index=True)

    track_uid: Mapped[Optional[str]] = mapped_column(ForeignKey("tracks.uid"))
    track: Mapped[Optional["GpsTrack"]] = relationship(back_populates="points")

    photos: Mapped[Optional[list["Photo"]]] = relationship(back_populates="gps_point")
    
    __table_args__ = (
        UniqueConstraint('track_uid', 'timestamp', name='_gps_unique_track_point'),
    )