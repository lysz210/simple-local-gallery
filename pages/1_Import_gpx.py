from pathlib import Path
from typing import List
from zoneinfo import ZoneInfo
import pandas as pd
from pydantic import BaseModel
import streamlit as st
import gpxpy as gpx
from datetime import datetime, timezone

from app.entities import GpsPoint, GpsTrack

class Point(BaseModel):
    time: datetime
    latitude: float
    longitude: float
    elevation: float | None
    type: str
    color: str
    name: str | None

    def from_gpx_point(other: gpx.mod_gpx.GPXTrackPoint) -> 'Point':
        return Point(
            time=other.time.astimezone(timezone.utc),
            latitude=other.latitude,
            longitude=other.longitude,
            elevation=other.elevation,
            type='point',
            color='#00ff00',
            name=None
        )
    
def to_entity_point(point: Point) -> GpsPoint:
    return GpsPoint(
        timestamp=point.time,
        latitude=point.latitude,
        longitude=point.longitude,
        elevation=point.elevation,
    )
        

st.set_page_config(
    page_title="Gpx",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])

def import_to_db(track_uid: int, track_name: str, points: list[Point]):
    db_file = gallery_root / 'photos.db'
    connection = st.connection(
        "photos",
        "sql",
        url=f"sqlite:///{db_file}"
    )
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


for gpx_path in gallery_root.glob('**/*.gpx'):
    
    doc = gpx.parse(gpx_path.open('r'))
    track_uid = doc.link.rsplit('-', 1)[-1]
    expander = st.expander(f"Track[{track_uid}] '{doc.name}'")

    if not expander.expanded:
        continue
    expander.write(gpx_path)
    if doc.time:
        expander.write(doc.time.astimezone(timezone.utc).astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M:%S"))
    expander.link_button(label="wikiloc page", url=doc.link)

    points: List[Point] = [Point.from_gpx_point(gpx_point) for point in doc.tracks for segment in point.segments for gpx_point in segment.points]

    gpx_table = pd.DataFrame.from_records([point.model_dump() for point in points]).set_index('time')

    expander.map(data=gpx_table, color='color', size=1.0)

    if expander.button("Import to database", key=doc.name):
        import_to_db(track_uid, doc.name, points)
