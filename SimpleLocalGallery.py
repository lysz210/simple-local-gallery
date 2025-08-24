from pathlib import Path
from tkinter.filedialog import askdirectory
from sqlalchemy import create_engine
import streamlit as st
from app import models

st.set_page_config(
    page_title="Simple Local Gallery",
)

st.markdown("# Simple Local Gallery")

def select_gallery_root():
    selected = askdirectory(title="Select Gallery Root Directory")
    st.session_state['gallery_root'] = selected

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

models.Base.metadata.create_all(connection.engine)
st.write(st.session_state['gallery_root'])
st.write(db_file)

with connection.session as s:
    photos = s.query(models.Photo).all()
    st.write(f"Found {len(photos)} photos in the database.")