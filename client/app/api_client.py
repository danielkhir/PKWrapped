import os
from io import BytesIO

import requests
from models import Pkm, PkmQuery, PkmStats, SaveStats, StatQuery


class APIClient:
    def __init__(self):
        self.BASE_URL = os.getenv("PKW_API_URL", "http://localhost:8000/")

    def get_pkms(self, pkm_query: PkmQuery) -> list[Pkm]:
        url = self.BASE_URL + "pkms/"
        url += f"?evTotal={pkm_query.evTotal}"
        url += f"&isNicknamed={pkm_query.isNicknamed}"
        url += f"&isShiny={pkm_query.isShiny}"
        url += f"&pageSize={pkm_query.pageSize}"
        url += f"&page={pkm_query.page}"

        pkms = requests.get(url).json()
        pkms = [Pkm.model_validate(pkm) for pkm in pkms]

        return pkms

    def get_random_pkm_ids(self) -> list[int]:
        url = self.BASE_URL + "pkms/random/"
        ids = requests.get(url).json()
        return ids

    def get_stats(self, stat_query: StatQuery) -> tuple[SaveStats, PkmStats]:
        url = self.BASE_URL + "stats/"
        url += f"?evTotal={stat_query.evTotal}"
        url += f"&isNicknamed={stat_query.isNicknamed}"
        url += f"&isShiny={stat_query.isShiny}"

        save_stats, pkm_stats = requests.get(url).json()
        save_stats = SaveStats.model_validate(save_stats)
        pkm_stats = PkmStats.model_validate(pkm_stats)

        return save_stats, pkm_stats

    def post_save(self, save: BytesIO) -> None:
        url = self.BASE_URL + "saves/"
        files = {"file": ("save", save)}
        requests.post(url, files=files)

    def delete_saves(self) -> None:
        url = self.BASE_URL + "saves/"
        requests.delete(url)
