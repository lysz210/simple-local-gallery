import streamlit as st


if 'photos' in st.session_state:
    photos = st.session_state['photos']
    for photo in photos:
        with st.container():
            st.write(photo.name)
            st.image(photo)