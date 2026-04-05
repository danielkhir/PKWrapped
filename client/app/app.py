import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import APIClient
from spritesheet import Spritesheet

spritesheet = Spritesheet()
client = APIClient()

st.set_page_config(
    page_title="home", page_icon="📈", layout="wide", initial_sidebar_state=10
)
st.title("PKWrapped - Box Analytics")


save_stats, pkm_stats = client.get_stats()

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
    st.plotly_chart(px.bar(pd.Series(pkm_stats.TopPkms)), key="top-mon-chart")
