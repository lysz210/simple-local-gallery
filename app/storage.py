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
import streamlit as st
from pathlib import Path

from app import models

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

def get_connection():
    return st.connection(
        "photos", type="sql",
         url=f"sqlite:///{Path(st.session_state['gallery_root']) / 'photos.db'}"
    )

def to_entity_point(point: models.Point) -> GpsPoint:
    return GpsPoint(
        timestamp=point.time,
        latitude=point.latitude,
        longitude=point.longitude,
        elevation=point.elevation,
    )

def save_track(track_uid: int, track_name: str, points: list[models.Point]):
    connection = get_connection()
    with connection.session as s:
        track = GpsTrack(
            uid=track_uid,
            name=track_name,
            description=None,
            points=[to_entity_point(point) for point in points]
        )
        s.add(track)
        s.commit()
    st.success(f"Imported {len(points)} points for track '{track_uid} - {track_name}'")

def count_photos() -> int:
    connection = get_connection()
    with connection.session as s:
        return s.query(Photo).count()

def tracks_summary():
    connection = get_connection()
    with connection.session as s:
        return s.query(
            GpsPoint.track_uid,
            func.count(GpsPoint.track).label('points_count'),
            func.min(GpsPoint.timestamp).label('start_time'),
            func.max(GpsPoint.timestamp).label('end_time'),
        ).group_by(GpsPoint.track_uid).all()