import streamlit as st
import gpxpy as gpx
import pandas as pd

st.set_page_config(
    page_title="Simple Local Gallery",
)

st.markdown("# Simple Local Gallery")

# points['time'].append(pd.to_datetime('2025-03-09 09:48:45+00:00'))
# points['latitude'].append(None)
# points['longitude'].append(None)
# points['elevation'].append(None)
# points['type'].append('photo')
#
# points['time'].append(pd.to_datetime('2025-03-09 09:49:15+00:00'))
# points['latitude'].append(None)
# points['longitude'].append(None)
# points['elevation'].append(None)
# points['type'].append('photo')
#
# table = (pd.DataFrame(points)
#          # set time as index
#          .set_index('time')
#          # reorder data-frame
#          .sort_index()
#          # interpolate values for photos
#          .interpolate())
# print(table.loc[[
#     pd.to_datetime('2025-03-09 09:48:15+00:00'),
#     pd.to_datetime('2025-03-09 09:48:45+00:00'),
#     pd.to_datetime('2025-03-09 09:49:15+00:00'),
#     pd.to_datetime('2025-03-09 09:49:50+00:00')
# ]])
# st.table(table)
