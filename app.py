import streamlit as st
import gpxpy as gpx
import pandas as pd

def configure_page() -> None:
    st.set_page_config(
        page_title="Simple Local Gallery",
    )

def main():
    configure_page()

    gpx_file = st.file_uploader("gpx file",
                                type='gpx',
                                accept_multiple_files=False,
                                key="gpx_file")

    photos = st.file_uploader("photos",
                              type="jpg",
                              accept_multiple_files=True,
                              key="photos")
    points = {
        'time': [],
        'latitude': [],
        'longitude': [],
        'elevation': [],
        'type': []
    }
    if gpx_file is not None:
        doc = gpx.parse(gpx_file)

        for track in doc.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points['time'].append(point.time)
                    points['latitude'].append(point.latitude)
                    points['longitude'].append(point.longitude)
                    points['elevation'].append(point.elevation)
                    points['type'].append('point')

    points['time'].append(pd.to_datetime('2025-03-09 09:48:45+00:00'))
    points['latitude'].append(None)
    points['longitude'].append(None)
    points['elevation'].append(None)
    points['type'].append('photo')

    points['time'].append(pd.to_datetime('2025-03-09 09:49:15+00:00'))
    points['latitude'].append(None)
    points['longitude'].append(None)
    points['elevation'].append(None)
    points['type'].append('photo')

    table = (pd.DataFrame(points)
             # set time as index
             .set_index('time')
             # reorder data-frame
             .sort_index()
             # interpolate values for photos
             .interpolate())
    print(table.loc[[
        pd.to_datetime('2025-03-09 09:48:15+00:00'),
        pd.to_datetime('2025-03-09 09:48:45+00:00'),
        pd.to_datetime('2025-03-09 09:49:15+00:00'),
        pd.to_datetime('2025-03-09 09:49:50+00:00')
    ]])
    st.table(table)


if __name__ == "__main__":
    main()