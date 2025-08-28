from pathlib import Path
from typing import List
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st
import gpxpy as gpx
from datetime import timezone

from app import storage
from app import models

st.set_page_config(
    page_title="Gpx",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])


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

    points: List[models.Point] = [models.from_gpx_point(gpx_point) for point in doc.tracks for segment in point.segments for gpx_point in segment.points]

    gpx_table = pd.DataFrame.from_records([point.model_dump() for point in points]).set_index('time')

    expander.map(data=gpx_table, color='color', size=1.0)

    if expander.button("Import to database", key=doc.name):
        storage.save_track(track_uid, doc.name, points)
