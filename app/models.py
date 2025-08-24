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

class Base(DeclarativeBase):
    pass

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    original_created_at: Mapped[datetime] = mapped_column()

    gps_point_id: Mapped[Optional[int]] = mapped_column(ForeignKey("points.id"))
    gps_point: Mapped[Optional["GpsPoint"]] = relationship(back_populates="photos")

class GpsPoint(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    track: Mapped[str] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    elevation: Mapped[Optional[float]] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.utcnow())

    photos: Mapped[Optional[list["Photo"]]] = relationship(back_populates="gps_point")
    
    __table_args__ = (
        UniqueConstraint('track', 'timestamp', name='_gps_unique_track_point'),
    )