import pandas as pd
import streamlit as st
import gpxpy as gpx
from datetime import timezone

st.set_page_config(
    page_title="Gpx",
)

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
    'color': []
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

table = pd.DataFrame.from_records(points).set_index('time')
st.session_state['gpx_info'] = table

st.map(data=table, color='color', size=1.0)
st.table(st.session_state['gpx_info'])