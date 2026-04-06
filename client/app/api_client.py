import os
import requests

from models import PkmStats, SaveStats


class APIClient:
    def __init__(self):
        self.BASE_URL = os.getenv("PKW_API_URL", "http://localhost:8000/")

    def get_pkmns(self, limit: int = 100):
        url = self.BASE_URL + f"pkms/?pageSize={limit}"
        pkms = requests.get(url).json()
        return pkms

    def get_random_pkm_ids(self):
        url = self.BASE_URL + "pkms/random"
        ids = requests.get(url).json()
        return ids

    def get_stats(self, ev_total: int = None):
        url = self.BASE_URL + "stats/"
        if ev_total:
            url += f"?evTotal={ev_total}"
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
