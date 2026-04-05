import streamlit as st
import pandas as pd
from app import spritesheet, client

st.set_page_config(page_title="box", page_icon="📦", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stElementToolbar"] {
    display: none !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "selected_sprite" not in st.session_state:
    st.session_state.selected_sprite = pd.Series()

df = pd.DataFrame(client.get_pkmns())

rows = 3
cols = 6
page_size = rows * cols
total_pages = (len(df) - 1) // page_size + 1

col_grid, col_info = st.columns([3, 2])

with col_grid:
    st.subheader("📦 Box")
    start_idx = st.session_state.current_page * page_size
    end_idx = start_idx + page_size
    current_batch = df[start_idx:end_idx]

    for r in range(rows):
        grid_rows = st.columns(cols, gap=None)
        for c in range(cols):
            batch_idx = r * cols + c

            with grid_rows[c]:
                if batch_idx < len(current_batch):
                    sprite = current_batch.iloc[batch_idx]

                    with st.container(
                        border=True,
                        width=128,
                        height=152,
                        horizontal_alignment="center",
                    ):
                        st.image(
                            spritesheet.get_sprite(sprite["FullSlug"]),
                            # caption=sprite['Nickname'],
                        )

                        if st.button(
                            f"{sprite['Nickname']}",
                            key=f"btn_{sprite['PID']}",
                            type="tertiary",
                        ):
                            st.session_state.selected_sprite = sprite
                else:
                    with st.container(
                        border=True,
                        width=128,
                        height=152,
                        horizontal_alignment="center",
                    ):
                        st.image(spritesheet.transparent_sprite, caption="")

    st.write("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button(
            "⬅️ Previous",
            use_container_width=True,
        ):
            if st.session_state.current_page == 0:
                st.session_state.current_page = total_pages - 1
            else:
                st.session_state.current_page -= 1
            st.rerun()
    with c2:
        st.markdown(
            f"<p style='text-align:center'>Page {st.session_state.current_page + 1} of {total_pages}</p>",
            unsafe_allow_html=True,
        )
    with c3:
        if st.button(
            "Next ➡️",
            use_container_width=True,
        ):
            if st.session_state.current_page == total_pages - 1:
                st.session_state.current_page = 0
            else:
                st.session_state.current_page += 1
            st.rerun()

# 4. Sidebar Inspector
with col_info:
    st.subheader("🔍 Info")
    if st.session_state.selected_sprite.any():
        s = st.session_state.selected_sprite
        with st.container(border=True, horizontal_alignment="center", height=600):
            st.image(
                spritesheet.get_sprite(s["FullSlug"]),
            )
            st.markdown(
                f"<p style='text-align: center;'>{s['Nickname']} the {s['Species']}</p>",
                unsafe_allow_html=True,
            )

            moves = s[["Move1", "Move2", "Move3", "Move4"]].to_list()
            moves = [f"\n- {m}" for m in moves if m != "(None)"]
            moves = "".join(moves)
            st.markdown(f"Nature: {s['Nature']}")
            st.markdown(f"Ability: {s['Ability']}")
            st.markdown(f"Level: {s['Level']}")
            st.markdown(f"OT: {s['OT']}")
            st.markdown(f"Met: {s['MetLoc']} ({s['Version']})")
            st.markdown(f"Moves: {moves}")
    else:
        st.info("Click on a name to see its data.")
