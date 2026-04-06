import os
import requests

from models import PkmStats, SaveStats, StatFilter, PkmFilter


class APIClient:
    def __init__(self):
        self.BASE_URL = os.getenv("PKW_API_URL", "http://localhost:8000/")

    def get_pkmns(self, pkm_filter: PkmFilter):
        url = self.BASE_URL + "pkms/"
        url += f"?evTotal={pkm_filter.evTotal}"
        url += f"&isNicknamed={pkm_filter.isNicknamed}"
        url += f"&isShiny={pkm_filter.isShiny}"
        url += f"&pageSize={pkm_filter.pageSize}"
        url += f"&page={pkm_filter.page}"
        pkms = requests.get(url).json()
        return pkms

    def get_random_pkm_ids(self):
        url = self.BASE_URL + "pkms/random/"
        ids = requests.get(url).json()
        return ids

    def get_stats(self, stat_filter: StatFilter):
        url = self.BASE_URL + "stats/"
        url += f"?evTotal={stat_filter.evTotal}"
        url += f"&isNicknamed={stat_filter.isNicknamed}"
        url += f"&isShiny={stat_filter.isShiny}"

        save_stats, pkm_stats = requests.get(url).json()
        save_stats = SaveStats.model_validate(save_stats)
        pkm_stats = PkmStats.model_validate(pkm_stats)
        return save_stats, pkm_stats

    def post_save(self, save):
        url = self.BASE_URL + "saves/"
        files = {"file": ("save", save)}
        requests.post(url, files=files)

    def delete_saves(self):
        url = self.BASE_URL + "saves/"
        requests.delete(url)
