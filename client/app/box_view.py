import streamlit as st
from spritesheet import Spritesheet


class BoxView:
    def __init__(self, n, spritesheet: Spritesheet, client, pkm_filter):
        self.rows = 3
        self.cols = 6
        self.page_size = self.rows * self.cols
        self.total_pages = (n - 1) // self.page_size + 1
        self.spritesheet = spritesheet
        self.client = client
        self.pkm_filter = pkm_filter

    def get_pkmns(self):
        self.pkm_filter.page = st.session_state.current_page
        return self.client.get_pkmns(self.pkm_filter)

    @st.fragment
    def view(self):
        pkms = self.get_pkmns()

        col_grid, col_info = st.columns([4, 2])

        with col_grid:
            st.subheader("📦 Box")
            current_batch = pkms

            for r in range(self.rows):
                grid_rows = st.columns(self.cols, gap=None)
                for c in range(self.cols):
                    batch_idx = r * self.cols + c

                    with grid_rows[c]:
                        if batch_idx < len(current_batch):
                            sprite = current_batch[batch_idx]

                            with st.container(
                                border=True,
                                width=120,
                                height=168,
                                horizontal_alignment="center",
                                gap="xxsmall",
                            ):
                                sprite_id = sprite["SpeciesID"]
                                is_shiny = sprite["IsShiny"]
                                has_species = sprite.get("SpeciesI", None)
                                if has_species:
                                    sprite_id = has_species["Sprite"]

                                st.image(
                                    self.spritesheet.get_sprite(sprite_id, is_shiny),
                                    # caption=sprite['Nickname'],
                                )

                                if st.button(
                                    f"{sprite['Nickname']}",
                                    key=f"btn_{sprite['ID']}",
                                    type="tertiary",
                                ):
                                    st.session_state.selected_sprite = sprite
                        else:
                            with st.container(
                                border=True,
                                width=120,
                                height=168,
                                horizontal_alignment="center",
                            ):
                                st.image(
                                    self.spritesheet.transparent_sprite, caption=""
                                )

            st.write("---")
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                if st.button(
                    "⬅️ Previous",
                    use_container_width=True,
                ):
                    if st.session_state.current_page == 0:
                        st.session_state.current_page = self.total_pages - 1
                    else:
                        st.session_state.current_page -= 1
                    st.rerun(scope="fragment")
            with c2:
                st.markdown(
                    f"<p style='text-align:center'>Page {st.session_state.current_page + 1} of {self.total_pages}</p>",
                    unsafe_allow_html=True,
                )
            with c3:
                if st.button(
                    "Next ➡️",
                    use_container_width=True,
                ):
                    if st.session_state.current_page == self.total_pages - 1:
                        st.session_state.current_page = 0
                    else:
                        st.session_state.current_page += 1
                    st.rerun(scope="fragment")

        with col_info:
            st.subheader("🔍 Info")
            if st.session_state.selected_sprite:
                s = st.session_state.selected_sprite
                with st.container(
                    border=True, horizontal_alignment="center", height=600
                ):
                    sprite_id = s["SpeciesID"]
                    is_shiny = s["IsShiny"]
                    has_species = s.get("SpeciesI", None)
                    if has_species:
                        sprite_id = has_species["Sprite"]
                    st.image(
                        self.spritesheet.get_sprite(sprite_id, is_shiny),
                    )
                    st.markdown(
                        f"<p style='text-align: center;'>{s['Nickname']} the {s['Species']}</p>",
                        unsafe_allow_html=True,
                    )

                    moves = [s[f"Move{x}"] for x in range(1, 5)]
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
