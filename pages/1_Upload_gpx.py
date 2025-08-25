from pathlib import Path
import pandas as pd
import streamlit as st
import gpxpy as gpx
from datetime import timezone

st.set_page_config(
    page_title="Gpx",
)

if 'gallery_root' not in st.session_state:
    st.switch_page("SimpleLocalGallery.py")

gallery_root = Path(st.session_state['gallery_root'])


for gpx_path in gallery_root.glob('**/*.gpx'):
    
    doc = gpx.parse(gpx_path.open('r'))
    track_id = doc.link.rsplit('-', 1)[-1]
    with st.expander(f"Track[{track_id}] '{doc.name}'"):
        st.write(gpx_path)
        st.link_button(label="wikiloc page", url=doc.link)


gpx_file = st.file_uploader("gpx file",
                            type='gpx',
                            accept_multiple_files=False,
                            key="gpx_file")
points = {
    'time': [],
    'latitude': [],
    'longitude': [],
    'elevation': [],
    'type': [],
    'color': [],
    'name': []
}
if gpx_file is not None:
    doc = gpx.parse(gpx_file)

    for track in doc.tracks:
        for segment in track.segments:
            for point in segment.points:
                points['time'].append(point.time.astimezone(timezone.utc))
                points['latitude'].append(point.latitude)
                points['longitude'].append(point.longitude)
                points['elevation'].append(point.elevation)
                points['type'].append('point')
                points['color'].append('#00ff00')
                points['name'].append(None)

table = pd.DataFrame.from_records(points).set_index('time')
st.session_state['gpx_info'] = table

st.map(data=table, color='color', size=1.0)
st.table(st.session_state['gpx_info'])