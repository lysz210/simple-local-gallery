from pathlib import Path
from tkinter.filedialog import askdirectory
import pandas as pd
from sqlalchemy import func
import streamlit as st
from app import storage


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
connection = storage.get_connection()

storage.Base.metadata.create_all(connection.engine)
st.write(st.session_state['gallery_root'])

st.write(f"Found {storage.count_photos()} photos in the database.")

st.table(pd.DataFrame(storage.tracks_summary()))

st.table(pd.DataFrame(storage.photos_summary()))