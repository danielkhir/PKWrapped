import streamlit as st
from api_client import APIClient
from models import Pkm, PkmQuery
from spritesheet import Spritesheet
from utils import undo_slug


class BoxView:
    def __init__(
        self,
        total_pkm: int,
        spritesheet: Spritesheet,
        client: APIClient,
        pkm_query: PkmQuery,
    ):
        self.rows = 3
        self.cols = 6
        self.page_size = self.rows * self.cols
        self.total_pages = (total_pkm - 1) // self.page_size + 1
        self.spritesheet = spritesheet
        self.client = client
        self.pkm_query = pkm_query

        self.cell_width = 120
        self.cell_height = 168

    def _get_pkmns(self) -> list[Pkm]:
        self.pkm_query.page = st.session_state.current_page
        return self.client.get_pkms(self.pkm_query)

    def _get_sprite(self, pkm: Pkm) -> str:
        sprite_id = pkm.SpeciesID
        if pkm.SpeciesInfo:
            sprite_id = pkm.SpeciesInfo.Sprite
        is_shiny = pkm.IsShiny

        return self.spritesheet.get_2dpkm(sprite_id, is_shiny)

    def _view_grid(self) -> None:
        pkms = self._get_pkmns()
        for r in range(self.rows):
            grid_rows = st.columns(self.cols, gap=None)
            for c in range(self.cols):
                idx = r * self.cols + c

                with grid_rows[c]:
                    if idx < len(pkms):
                        pkm = pkms[idx]

                        with st.container(
                            border=True,
                            width=self.cell_width,
                            height=self.cell_height,
                            horizontal_alignment="center",
                            gap="xxsmall",
                        ):
                            st.image(self._get_sprite(pkm))

                            if st.button(
                                f"{pkm.Nickname}",
                                key=f"btn_{pkm.ID}",
                                type="tertiary",
                            ):
                                st.session_state.selected_sprite = pkm
                    else:
                        with st.container(
                            border=True,
                            width=self.cell_width,
                            height=self.cell_height,
                            horizontal_alignment="center",
                        ):
                            st.image(self.spritesheet.transparent_sprite, caption="")

        # Page selector
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

    def _view_info(self) -> None:
        if st.session_state.selected_sprite:
            pkm: Pkm = st.session_state.selected_sprite

            with st.container(border=True, horizontal_alignment="center", height=600):
                st.image(self._get_sprite(pkm))
                st.markdown(
                    f"<p style='text-align: center;'>{pkm.Nickname} ({pkm.Species.capitalize()})</p>",
                    unsafe_allow_html=True,
                )

                moves = [pkm.Move1, pkm.Move2, pkm.Move3, pkm.Move4]
                moves = [f"\n- {undo_slug(move)}" for move in moves]
                moves = "".join(moves)

                st.markdown(f"Nature: {pkm.Nature.capitalize()}")
                st.markdown(f"Ability: {undo_slug(pkm.Ability)}")
                st.markdown(f"Level: {pkm.Level}")
                st.markdown(f"OT: {pkm.OT}")
                st.markdown(f"Met: {pkm.MetLoc} ({pkm.Version})")
                st.markdown(f"Moves: {moves}")
        else:
            st.info("Click on a Mon to see its data.")

    @st.fragment
    def view(self) -> None:
        col_grid, col_info = st.columns([4, 2])
        with col_grid:
            st.subheader("📦 Box")
            self._view_grid()

        with col_info:
            st.subheader("🔍 Info")
            self._view_info()
