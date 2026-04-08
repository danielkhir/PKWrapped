import streamlit as st
from api_client import APIClient
from box_view import BoxView
from elements import HideFSButton, SpriteMarquee, SpriteRow
from models import PkmQuery, StatQuery
from spritesheet import Spritesheet
from utils import undo_slug

# Setup dependencies
spritesheet = Spritesheet()
client = APIClient()

# Setup page matter
st.set_page_config(
    page_title="home", page_icon="📈", layout="wide", initial_sidebar_state=10
)
st.markdown(HideFSButton, unsafe_allow_html=True)

st.title("PKWrapped - Box Analytics")

# Setup session state
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "selected_sprite" not in st.session_state:
    st.session_state.selected_sprite = dict()

# Sidebar
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
    stat_query = StatQuery(
        evTotal=510 if options[0] in settings_selection else 0,
        isNicknamed=True if options[1] in settings_selection else False,
        isShiny=True if options[2] in settings_selection else False,
    )
    save_stats, pkm_stats = client.get_stats(stat_query)

    if st.button("Wipe data", type="tertiary"):
        client.delete_saves()
        st.rerun()

if save_stats.TotalSaves < 1:
    st.info("You have no saves. Upload one!")
    st.stop()

# Marquee
marquee_pkms = [spritesheet.get_3dpkm(id) for id in client.get_random_pkm_ids()]
st.iframe(SpriteMarquee(marquee_pkms), height=72)

# Metrics
st.markdown("## Overall Metrics")
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


# Top X
st.markdown("## Top Used")
col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    st.subheader("Mons")
    images = [
        (
            spritesheet.get_3dpkm(species_id),
            count["Species"].capitalize(),
            count["count"],
        )
        for species_id, count in pkm_stats.TopPkms.items()
    ]
    st.markdown(SpriteRow(images), unsafe_allow_html=True)
with col2:
    st.subheader("Balls")
    images = [
        (
            spritesheet.get_item(ball),
            undo_slug(ball),
            count,
        )
        for ball, count in pkm_stats.TopBalls.items()
    ]

    st.markdown(SpriteRow(images), unsafe_allow_html=True)
with col3:
    st.subheader("Held Items")
    images = [
        (
            spritesheet.get_item(item),
            undo_slug(item),
            count,
        )
        for item, count in pkm_stats.TopHeldItems.items()
    ]

    st.markdown(SpriteRow(images), unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    st.subheader("Types")
    images = [
        (
            spritesheet.get_type(ty),
            undo_slug(ty),
            count,
        )
        for ty, count in pkm_stats.TopPkmTypes.items()
    ]

    st.markdown(SpriteRow(images), unsafe_allow_html=True)
with col2:
    st.subheader("Moves")
    images = [
        (
            spritesheet.get_type(move_info["Type"]),
            undo_slug(move),
            move_info["count"],
        )
        for move, move_info in pkm_stats.TopMoves.items()
    ]
    st.markdown(SpriteRow(images), unsafe_allow_html=True)

st.write("")

# Box View
st.markdown("## Box Browser")
pkm_query = PkmQuery(
    evTotal=510 if options[0] in settings_selection else 0,
    isNicknamed=True if options[1] in settings_selection else False,
    isShiny=True if options[2] in settings_selection else False,
    pageSize=18,
    page=st.session_state.current_page,
)
box_view = BoxView(pkm_stats.TotalPkm, spritesheet, client, pkm_query)
box_view.view()
