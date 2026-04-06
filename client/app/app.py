import streamlit as st

from api_client import APIClient
from elements import SpriteMarquee, HideFSButton, SpriteRow
from spritesheet import Spritesheet
from models import StatFilter, PkmFilter
from box_view import BoxView

spritesheet = Spritesheet()
client = APIClient()

st.set_page_config(
    page_title="home", page_icon="📈", layout="wide", initial_sidebar_state=10
)
st.markdown(HideFSButton, unsafe_allow_html=True)

st.title("PKWrapped - Box Analytics")

st.iframe(SpriteMarquee(client.get_random_pkm_ids()), height=72)

# save_stats, pkm_stats = client.get_stats(StatFilter())

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "selected_sprite" not in st.session_state:
    st.session_state.selected_sprite = dict()

with st.sidebar:
    uploaded_file = st.file_uploader("Upload a save.", max_upload_size=1)

    if uploaded_file is not None:
        if not st.session_state.file_processed:
            st.session_state.file_processed = True
            bytes_data = uploaded_file.getvalue()
            client.post_save(bytes_data)
            st.rerun()
    if uploaded_file is None and st.session_state.file_processed:
        st.session_state.file_processed = False

    st.subheader("Settings")
    options = ["Max EVs", "Nicknamed", "Shiny"]
    settings_selection = st.pills("Filters", options, selection_mode="multi")
    stat_filter = StatFilter(
        evTotal=510 if options[0] in settings_selection else 0,
        isNicknamed=True if options[1] in settings_selection else False,
        isShiny=True if options[2] in settings_selection else False,
    )
    save_stats, pkm_stats = client.get_stats(stat_filter)

    if st.button("Wipe data", type="tertiary"):
        client.delete_saves()
        st.rerun()

if save_stats.TotalSaves < 1:
    st.text("You have no saves. Upload one!")


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
# col1, col2 = st.columns(2)
# with col1:
#     st.subheader("Top 5 Moves")
#     st.plotly_chart(px.bar(pd.Series(pkm_stats.TopMoves)), key="top-move-chart")
# with col2:
st.subheader("Top 5 Mons")
images = [
    (f"{spritesheet.sprite3d_url}{species_id}.gif", count)
    for species_id, count in pkm_stats.TopPkms.items()
]
st.markdown(SpriteRow(images), unsafe_allow_html=True)


pkm_filter = PkmFilter(
    evTotal=510 if options[0] in settings_selection else 0,
    isNicknamed=True if options[1] in settings_selection else False,
    isShiny=True if options[2] in settings_selection else False,
    pageSize=18,
    page=st.session_state.current_page,
)
box_view = BoxView(pkm_stats.TotalPkm, spritesheet, client, pkm_filter)
box_view.view()
