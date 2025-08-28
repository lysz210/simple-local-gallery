import streamlit as st
from tkinter.filedialog import askopenfilename
from app.entities import Photo

st.set_page_config(
    page_title="Simple Local Gallery",
)

st.markdown("# Simple Local Gallery")

def db_file_handler():
    db_file_name = askopenfilename(filetypes=[("SQLite", ".sqlite .db")])
    st.session_state['db_file'] = db_file_name
# FIXME: da rimuovere.
# tmp code to avoid the annoing askopenfile dialog
# witch isn't very nice
st.session_state['db_file'] = '/home/lysz210/PycharmProjects/simple-local-gallery/photos.db'

if 'db_file' not in st.session_state:
    st.button("Seleziona il file sqlite", on_click=db_file_handler)
else:
    st.write(st.session_state['db_file'])
    connection = st.connection(
        "photos",
        "sql",
        url=f"sqlite:///{st.session_state['db_file']}"
    )
    with connection.session as s:
        q = s.query(
            Photo
        )
        st.write(q.all())


