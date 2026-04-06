import re

from PIL import Image


class Spritesheet:
    def __init__(self):
        self.base_path = "./static/"
        self.spritesheet_path = self.base_path + "pokesprite-pokemon-gen8.png"
        self.spritecss_path = self.base_path + "pokesprite-pokemon-gen8.css"

        self.sprite3d_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/"

        self.spritesheet = None
        self.spritecss = None
        self.sprite_size = (0, 0)
        self.sprite_coordinates = dict()

        self.resized_ = 64

        self.transparent_sprite = Image.new(
            "RGBA", (self.resized_, self.resized_), (0, 0, 0, 0)
        )

        self._load_spritesheet()
        self._parse_spritesheet()

    def _load_spritesheet(self):
        self.spritesheet = Image.open(self.spritesheet_path)

        with open(self.spritecss_path, "r") as f:
            self.spritecss = f.read()

    def _parse_spritesheet(self):
        sprite_size = re.findall(r"(width|height): (\d+)px", self.spritecss)
        sprite_width = [int(x[1]) for x in sprite_size if x[0] == "width"][0]
        sprite_height = [int(x[1]) for x in sprite_size if x[0] == "height"][0]
        self.sprite_size = (sprite_width, sprite_height)

        parsed_spritecss = re.findall(
            r"(pokesprite)\.(.+)\s\{\n\s+(background-position):\s-(\d+)px\s-(\d+)px;",
            self.spritecss,
        )
        for sprite in parsed_spritecss:
            self.sprite_coordinates[sprite[1]] = (int(sprite[3]), int(sprite[4]))

    def get_sprite(self, pkmn):
        x, y = self.sprite_coordinates.get(pkmn, (None, None))
        if x is None or y is None:
            return self.transparent_sprite

        return self.spritesheet.crop(
            (x, y, x + self.sprite_size[0], y + self.sprite_size[1])
        ).resize((self.resized_, self.resized_))
