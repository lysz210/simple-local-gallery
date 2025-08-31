import base64
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from zoneinfo import ZoneInfo
import piexif
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

from app import storage

type point_value = int
type point_multiplier = int
type point_sub = tuple[point_value, point_multiplier]

type point = tuple[point_sub, point_sub, point_sub]
type altitude_point = point_sub

def dec_to_dms(dec: float,
               seconds_multiplier: point_multiplier = 10000,
               ) -> point:
    '''
    Convert decimal degrees to degrees-minutes-seconds

    Parameters
    ----------
    dec : float
        Input coordinate in decimal degrees.

    Returns
    -------
    list
        Coordinate in degrees-minutes-seconds.
        :param dec:
        :param minutes_multiplier:
        :param degrees_multiplier:
        :param seconds_multiplier:
    '''
    degree = int(np.floor(dec))
    minutes = dec % 1.0 * 60
    seconds = int(np.floor(minutes % 1.0 * 60 * seconds_multiplier))
    minutes = int(np.floor(minutes))

    return (degree, 1), (minutes, 1), (seconds, seconds_multiplier)

def normalize_alt(dec: float|int, altitude_multiplier = 1000) -> altitude_point:
    if dec is int:
        return dec, 1
    value = np.floor(dec * altitude_multiplier)
    return int(value), altitude_multiplier

gallery_root = Path(st.session_state['gallery_root'])

photos_summary = storage.photos_summary()

select_photos_dir = st.selectbox(
    'Select photo to geotag',
    photos_summary,
    format_func=lambda photo: f"'{photo.path}' with {photo.photos_count} Photos"
)

st.write(select_photos_dir)

photos = storage.get_photos_in_folder(select_photos_dir.path)

photos_table = []

for photo in photos:
    image_path = gallery_root / photo.path / photo.filename
    image = Image.open(image_path)
    data = photo.to_dict()
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    data['image'] = f"data:image/jpeg;base64,{img_str.decode()}"
    photos_table.append(data)

st.dataframe(photos_table,
             column_config={
                 'image': st.column_config.ImageColumn(
                     "Image",
                     help="Photo preview",
                     width=240,
                 ),
             },
             hide_index=True,
             row_height=240
             )

# with st.form("photo_selection_form"):
#     for photo in photos:
#         st.checkbox(f"Select {photo.filename}", key=photo.id, value=False)
#         st.write(photo.filename)
#         image_path = gallery_root / photo.path / photo.filename
#         image = Image.open(image_path)
#         image = ImageOps.exif_transpose(image)
#         st.image(image)
#     st.form_submit_button("Select Photos")

# mapped_photos = st.session_state['interpolated_df']
# st.map(data=mapped_photos, color='color', size=1.0)

# if 'photos' in st.session_state:
#     photos = st.session_state['photos']
#     for image in photos:
#         with st.container():
#             st.write(image.name)
#             st.image(image)

# if st.button('Save', type="primary"):
#     photos_dict = {row['name']: row for row in mapped_photos.to_dict(orient='records')}
#     print(photos_dict)
#     europe_rome = ZoneInfo('Europe/Rome')
#     for photo in photos:
#         image = Image.open(photo)
#         meta = photos_dict.get(photo.name)
#         lat = dec_to_dms(meta['latitude'])
#         lng = dec_to_dms(meta['longitude'])
#         alt = normalize_alt(meta['elevation'])
#         exif = piexif.load(image.info["exif"])
#         metas = exif["Exif"]
#         created_at = metas[piexif.ExifIFD.DateTimeOriginal]
#         originalDatetime = (datetime
#                                 .strptime(created_at.decode('utf8'), "%Y:%m:%d %H:%M:%S")
#                                 .astimezone(europe_rome).astimezone(timezone.utc)
#                             )
#         new_date = originalDatetime.strftime("%Y:%m:%d")
#         new_time = (originalDatetime.hour, 1), (originalDatetime.minute, 1), (originalDatetime.second, 1)
#         gps = exif['GPS']
#         gps[piexif.GPSIFD.GPSLatitude] = lat
#         gps[piexif.GPSIFD.GPSLatitudeRef] = 'N' if meta['latitude'] >= 0 else 'S'
#         gps[piexif.GPSIFD.GPSLongitude] = lng
#         gps[piexif.GPSIFD.GPSLongitudeRef] = 'E' if meta['longitude'] >= 0 else 'W'
#         gps[piexif.GPSIFD.GPSAltitude] = alt
#         gps[piexif.GPSIFD.GPSDateStamp] = new_date
#         gps[piexif.GPSIFD.GPSTimeStamp] = new_time

#         exif_bytes = piexif.dump(exif)
#         image.save(f"images/{photo.name}", exif=exif_bytes, quality=100)
#         st.write(photo.name)
#         st.write(meta)