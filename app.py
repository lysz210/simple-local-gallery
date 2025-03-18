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

    if gpx_file is not None:
        doc = gpx.parse(gpx_file)
        points = {
            'time': [],
            'latitude': [],
            'longitude': [],
            'elevation': [],
        }
        for track in doc.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points['time'].append(point.time)
                    points['latitude'].append(point.latitude)
                    points['longitude'].append(point.longitude)
                    points['elevation'].append(point.elevation)

        st.table(pd.DataFrame(points))


if __name__ == "__main__":
    main()