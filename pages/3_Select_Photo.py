from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import piexif
import streamlit as st
import numpy as np
from PIL import Image

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

st.markdown("# Working in progress...")
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