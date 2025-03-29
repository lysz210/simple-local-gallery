from typing import Optional
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    DateTime
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
    filename: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    original_created_at: Mapped[datetime] = mapped_column()

    gps_point_id: Mapped[int] = mapped_column(ForeignKey("points.id"))
    gps_point: Mapped[Optional["GpsPoint"]] = relationship(back_populates="photos")

class GpsPoint(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    elevation: Mapped[Optional[float]] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    photos: Mapped[Optional[list["Photo"]]] = relationship(back_populates="gps_point")