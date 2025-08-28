from collections import Counter
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
import piexif
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Photos",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])

photos_paths = [p for p in gallery_root.rglob('*.jpg', case_sensitive=False)]

folder_counts = Counter(str(p.parent) for p in photos_paths)

st.write(folder_counts)

# si potrebbe utilizzare il upsert ma questo significa modificare una marea di righe

# soluzione alternativa e' recuperare la lista degli elementi presenti a db
# e inserire solo quelli che non sono presenti
# potenziale rischio di aggiornare file.
# ma trattandosi di foto originali probabilmente non e' un problema
# in questo caso 