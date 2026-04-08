import os
import sqlite3
import time

import pandas as pd
import requests
from tqdm.auto import tqdm

DB_PATH = os.getenv("PKW_DB_URL", "./data/test.sqlite")


class SpeciesETL:
    def __init__(self):
        self.forme_url = "https://pokeapi.co/api/v2/pokemon-form/"
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species/"

    def _fetch_ids(self) -> list[int]:
        res = requests.get(f"{self.forme_url}/?limit=1600&offset=0").json()["results"]
        return [int(item["url"].split("/")[-2]) for item in res]

    def _fetch_form(self, id: int) -> dict:
        forme_res = requests.get(f"{self.forme_url}{id}/").json()

        types = forme_res["types"]
        type1 = types[0]["type"]["name"]
        if len(types) == 2:
            type2 = types[1]["type"]["name"]
        else:
            type2 = "none"

        sprite = forme_res["sprites"]["front_default"]
        if sprite is None:
            sprite = id
        else:
            sprite = sprite.split("/")[-1][:-4]

        species_id = int(forme_res["pokemon"]["url"].split("/")[-2])
        if species_id < 10000:
            species_res = requests.get(f"{self.species_url}{species_id}/").json()
        else:
            species_res = {
                "is_baby": False,
                "is_legendary": False,
                "is_mythical": False,
                "name": forme_res["name"],
            }

        return {
            "FormID": id,
            "SpeciesID": species_id,
            "FormName": forme_res["name"],
            "SpeciesName": species_res["name"],
            "Sprite": sprite,
            "Type1": type1,
            "Type2": type2,
            "IsBaby": species_res["is_baby"],
            "IsLegendary": species_res["is_legendary"],
            "IsMythical": species_res["is_mythical"],
        }

    def extract(self) -> pd.DataFrame:
        ids = self._fetch_ids()
        fetch_per_loop = 500
        n_loops = len(ids) // fetch_per_loop

        species = []
        idxs = [fetch_per_loop * loop for loop in range(n_loops)] + [len(ids)]

        for start, stop in zip(idxs, idxs[1:]):
            print(f"Fetching ids {start} - {stop}")
            id_subset = ids[start:stop]
            for id in tqdm(id_subset):
                species.append(self._fetch_form(id))
            time.sleep(3)

        return pd.DataFrame(species)

    def transform(self, species_df: pd.DataFrame) -> pd.DataFrame:
        gender_suffix = r"-(?:fe)?(?:male)"
        gender_suffix_in_species = species_df.SpeciesName.str.contains(gender_suffix)
        species_df.loc[gender_suffix_in_species, "SpeciesName"] = species_df[
            gender_suffix_in_species
        ]["SpeciesName"].str.replace(gender_suffix, "", regex=True)
        return species_df

    def load(self, species_df: pd.DataFrame) -> pd.DataFrame:
        species_df = species_df.set_index("FormID")

        con = sqlite3.connect(DB_PATH)
        res = species_df.to_sql(name="species", con=con, if_exists="replace")
        con.commit()
        con.close()
        print(f"Committed {res} records.")

        return species_df


class MoveETL:
    def __init__(self):
        self.move_url = "https://pokeapi.co/api/v2/move/"

    def _fetch_ids(self) -> list[int]:
        res = requests.get(f"{self.move_url}/?limit=1000&offset=0").json()["results"]
        return [int(item["url"].split("/")[-2]) for item in res]

    def _fetch_move(self, id: int) -> dict:
        move_res = requests.get(f"{self.move_url}{id}/").json()

        return {
            "ID": id,
            "Name": move_res["name"],
            "Type": move_res["type"]["name"],
            "Power": move_res["power"],
            "PP": move_res["pp"],
            "Accuracy": move_res["accuracy"],
            "DamageClass": move_res["damage_class"]["name"],
        }

    def extract(self) -> pd.DataFrame:
        ids = self._fetch_ids()
        fetch_per_loop = 500
        n_loops = len(ids) // fetch_per_loop

        moves = []
        idxs = [fetch_per_loop * loop for loop in range(n_loops)] + [len(ids)]

        for start, stop in zip(idxs, idxs[1:]):
            print(f"Fetching ids {start} - {stop}")
            id_subset = ids[start:stop]
            for id in tqdm(id_subset):
                moves.append(self._fetch_move(id))
            time.sleep(3)

        return pd.DataFrame(moves)

    def transform(self, move_df: pd.DataFrame) -> pd.DataFrame:
        return move_df

    def load(self, move_df: pd.DataFrame) -> pd.DataFrame:
        move_df = move_df.set_index("ID")

        con = sqlite3.connect(DB_PATH)
        res = move_df.to_sql(name="move", con=con, if_exists="replace")
        con.commit()
        con.close()
        print(f"Committed {res} records.")

        return move_df


if __name__ == "__main__":
    path = "./data/moves.json"
    if os.path.exists(path):
        move_df = pd.read_json(path)
        MoveETL().load(move_df)
    else:
        print("Fetching moves.")
        move_etl = MoveETL()
        move_df = move_etl.extract()
        move_df = move_etl.transform(move_df)

        move_df.to_json(path)
        move_df = move_etl.load(move_df)

    path = "./data/species.json"
    if os.path.exists(path):
        species_df = pd.read_json(path)
        SpeciesETL().load(species_df)
    else:
        print("Fetching species.")
        species_etl = SpeciesETL()
        species_df = species_etl.extract()
        species_df = species_etl.transform(species_df)

        species_df.to_json(path)
        species_df = species_etl.load(species_df)

    print("Done.")
