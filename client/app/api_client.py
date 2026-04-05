import os
import requests

from models import PkmStats, SaveStats


class APIClient:
    def __init__(self):
        self.BASE_URL = os.getenv("PKW_API_URL", "http://localhost:8000/")

    def get_pkmns(self, limit: int = 100):
        url = self.BASE_URL + f"pkms/?page_size={limit}"
        pkms = requests.get(url).json()
        return pkms

    def get_stats(self):
        url = self.BASE_URL + "stats/"
        save_stats, pkm_stats = requests.get(url).json()
        save_stats = SaveStats.model_validate(save_stats)
        pkm_stats = PkmStats.model_validate(pkm_stats)
        return save_stats, pkm_stats
