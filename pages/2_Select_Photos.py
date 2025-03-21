import pandas as pd
import streamlit as st
from PIL import Image
import piexif
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Photos",
)

photos_files = st.file_uploader("Photos",
                            type=['jpg', 'jpeg'],
                            accept_multiple_files=True,
                            key="photos_files")
points = {
    'time': [],
    'latitude': [],
    'longitude': [],
    'elevation': [],
    'type': [],
    'color': []
}
if photos_files is not None:
    europe_rome = ZoneInfo('Europe/Rome')
    for photo_file in photos_files:
        image = Image.open(photo_file)
        if 'exif' not in image.info:
            continue
        matadata = piexif.load(image.info["exif"])
        exif = matadata["Exif"]
        created_at = exif[piexif.ExifIFD.DateTimeOriginal]
        created_offset = exif[piexif.ExifIFD.OffsetTimeOriginal]
        originalDatetime = (datetime
                                .strptime(created_at.decode('utf8'), "%Y:%m:%d %H:%M:%S")
                                .astimezone(europe_rome).astimezone(timezone.utc)
                            )
        # TODO: skip if originalDatetime is outside pgx to avoid incorrect interpretation
        points['time'].append(originalDatetime)
        points['type'].append('photo')
        points['color'].append('#0000ff')
        points['latitude'].append(None)
        points['longitude'].append(None)
        points['elevation'].append(None)

photos_table = pd.DataFrame.from_records(points).set_index('time')

joined_table = pd.concat([st.session_state['gpx_info'], photos_table])
joined_table.sort_index(inplace=True)
joined_table.interpolate(inplace=True)
st.markdown("# Photos")
st.map(data=joined_table, color='color', size=1.0)
st.write(joined_table)


st.write(st.session_state['gpx_info'])