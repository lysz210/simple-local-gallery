from pathlib import Path
from tkinter.filedialog import askdirectory
import pandas as pd
from sqlalchemy import func
import streamlit as st
from app import entities


st.set_page_config(
    page_title="Simple Local Gallery",
)

st.markdown("# Simple Local Gallery")

def select_gallery_root():
    selected = askdirectory(title="Select Gallery Root Directory")
    st.session_state['gallery_root'] = selected
st.session_state['gallery_root'] = '/home/lysz210/PycharmProjects/simple-local-gallery/upload'

if 'gallery_root' not in st.session_state:
    st.info("Please select the root directory of your photo gallery.")
    st.button("Select Gallery Root Directory", on_click=select_gallery_root)
    st.stop()

gallery_root = Path(st.session_state['gallery_root'])

db_file = gallery_root / 'photos.db'
connection = st.connection(
    "photos",
    "sql",
    url=f"sqlite:///{db_file}"
)

entities.Base.metadata.create_all(connection.engine)
st.write(st.session_state['gallery_root'])
st.write(db_file)

with connection.session as s:
    photos_count = s.query(entities.Photo).count()
    st.write(f"Found {photos_count} photos in the database.")
    tracks_aggragation = s.query(
            entities.GpsPoint.track_uid,
            func.count(entities.GpsPoint.track).label('points_count'),
            func.min(entities.GpsPoint.timestamp).label('start_time'),
            func.max(entities.GpsPoint.timestamp).label('end_time'),
        ).group_by(entities.GpsPoint.track_uid).all()
    st.write(tracks_aggragation)
    st.table(pd.DataFrame(tracks_aggragation))
