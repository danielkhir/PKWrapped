from PIL import Image
from models import TYPES


class Spritesheet:
    def __init__(self):
        self.base_url = (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/"
        )
        self.pkm3d_url = self.base_url + "pokemon/other/showdown/"
        self.pkm2d_url = self.base_url + "pokemon/"
        self.item_url = self.base_url + "items/"
        self.type_url = self.base_url + "types/generation-ix/scarlet-violet/small/"

        self.sprite_size = 96

        self.transparent_sprite = Image.new(
            "RGBA", (self.sprite_size, self.sprite_size), (0, 0, 0, 0)
        )

    def get_2dpkm(self, id: str, is_shiny=False) -> str:
        if is_shiny:
            return self.pkm2d_url + "shiny/" + f"{id}.png"
        return self.pkm2d_url + f"{id}.png"

    def get_3dpkm(self, id: str) -> str:
        return self.pkm3d_url + f"{id}.gif"

    def get_item(self, id: str) -> str:
        # handle z-crystals
        if "-z" in id:
            id = id + "--bag"
        return self.item_url + f"{id}.png"

    def get_type(self, id: str) -> str:
        return self.type_url + f"{TYPES[id]}.png"
