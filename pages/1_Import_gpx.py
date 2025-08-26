from pathlib import Path
from typing import TypedDict
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st
import gpxpy as gpx
from datetime import datetime, timezone

from app.models import GpsPoint

class Point(TypedDict):
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
    
def to_model_point(track_id: int, track: str, point: Point) -> GpsPoint:
    return GpsPoint(
        track_id=track_id,
        track=track,
        timestamp=point['time'],
        latitude=point['latitude'],
        longitude=point['longitude'],
        elevation=point['elevation'],
    )
        

st.set_page_config(
    page_title="Gpx",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])

def import_to_db(track_id: int, track_name: str, points: list[Point]):
    db_file = gallery_root / 'photos.db'
    connection = st.connection(
        "photos",
        "sql",
        url=f"sqlite:///{db_file}"
    )
    with connection.session as s:
        s.add_all([to_model_point(track_id, track_name, point) for point in points])
        s.commit()
    st.success(f"Imported {len(points)} points for track '{track_id} - {track_name}'")


for gpx_path in gallery_root.glob('**/*.gpx'):
    
    doc = gpx.parse(gpx_path.open('r'))
    track_id = int(doc.link.rsplit('-', 1)[-1])
    expander = st.expander(f"Track[{track_id}] '{doc.name}'")
    if not expander.expanded:
        continue
    expander.write(gpx_path)
    if doc.time:
        expander.write(doc.time.astimezone(timezone.utc).astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M:%S"))
    expander.link_button(label="wikiloc page", url=doc.link)

    points = [Point.from_gpx_point(gpx_point) for point in doc.tracks for segment in point.segments for gpx_point in segment.points]

    gpx_table = pd.DataFrame.from_records(points).set_index('time')

    expander.map(data=gpx_table, color='color', size=1.0)

    if expander.button("Import to database", key=doc.name):
        import_to_db(track_id, doc.name, points)
