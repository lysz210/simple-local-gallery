from collections import Counter
from pathlib import Path
from typing import List
import pandas as pd
import streamlit as st
from PIL import Image
import piexif
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app import storage

st.set_page_config(
    page_title="Photos",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])

photos_paths = [p.relative_to(gallery_root) for p in gallery_root.rglob('*.jpg', case_sensitive=False)]

folder_groups: dict[str, List[Path]] = {}

for photo_path in photos_paths:
    folder = str(photo_path.parent)
    if folder not in folder_groups:
        folder_groups[folder] = []
    folder_groups[folder].append(photo_path)

def save_photo(expander, photo_files: List[Path]):
    storage.save_photos(gallery_root, photo_files)
    expander.write('Photos imported.')

@st.fragment
def show_photo_expander(photo_path: Path, photo_files: list[Path]):
    expander = st.expander(f"Photo: {photo_path.name} ({len(photo_files)} files)")
    if expander.expanded:
        if expander.button("Import to database", key=str(photo_path)):
            save_photo(expander, photo_files)

for folder, paths in folder_groups.items():
    show_photo_expander(Path(folder), paths)
        

# si potrebbe utilizzare il upsert ma questo significa modificare una marea di righe

# soluzione alternativa e' recuperare la lista degli elementi presenti a db
# e inserire solo quelli che non sono presenti
# potenziale rischio di aggiornare file.
# ma trattandosi di foto originali probabilmente non e' un problema
# in questo caso 