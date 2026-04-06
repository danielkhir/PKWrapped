import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import APIClient
from elements import SpriteMarquee, HideFSButton, SpriteRow
from spritesheet import Spritesheet

spritesheet = Spritesheet()
client = APIClient()

st.set_page_config(
    page_title="home", page_icon="📈", layout="wide", initial_sidebar_state=10
)
st.markdown(HideFSButton, unsafe_allow_html=True)

st.title("PKWrapped - Box Analytics")

st.iframe(SpriteMarquee(client.get_random_pkm_ids()), height=72)

save_stats, pkm_stats = client.get_stats()
if save_stats.TotalSaves < 1:
    st.text("You have no saves. Upload one!")

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

with st.expander("Settings", expanded=True):
    uploaded_file = st.file_uploader("Upload a save.", max_upload_size=1)

    if uploaded_file is not None:
        if not st.session_state.file_processed:
            st.session_state.file_processed = True
            bytes_data = uploaded_file.getvalue()
            client.post_save(bytes_data)
            st.rerun()
    if uploaded_file is None and st.session_state.file_processed:
        st.session_state.file_processed = False

    col1, col2 = st.columns(2)
    with col1:
        options = ["Max EVs", "Nicknamed"]
        selection = st.segmented_control("Filters", options, selection_mode="multi")
        if options[0] in selection:
            save_stats, pkm_stats = client.get_stats(510)
    with col2:
        if st.button("Wipe data"):
            client.delete_saves()
            st.rerun()


st.subheader("Overall Metrics")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Saves")
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        st.metric("Total Saves", save_stats.TotalSaves)
    with subcol2:
        st.metric("Total Hours", round(save_stats.TotalPlayedSeconds / 3600, 2))
        st.metric("Total Money", save_stats.TotalMoney)

with col2:
    st.subheader("PKMs")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pokemon", pkm_stats.TotalPkm)
        st.metric("Unique Species", pkm_stats.TotalUniqueSpecies)
    with col2:
        st.metric("Perfect IVs", pkm_stats.TotalPerfectIVs)
        st.metric("Max EVs", pkm_stats.TotalMaxEVs)
    with col3:
        st.metric("Shinies", pkm_stats.TotalShinies)
        st.metric("Nicknamed", pkm_stats.TotalNicknamed)


st.subheader("Top Used")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Moves")
    st.plotly_chart(px.bar(pd.Series(pkm_stats.TopMoves)), key="top-move-chart")
with col2:
    st.subheader("Top 5 Mons")
    images = [
        (f"{spritesheet.sprite3d_url}{species_id}.gif", count)
        for species_id, count in pkm_stats.TopPkms.items()
    ]
    st.markdown(SpriteRow(images), unsafe_allow_html=True)
