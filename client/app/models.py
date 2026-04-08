from typing import Optional
from pydantic import BaseModel


class PkmStats(BaseModel):
    TotalPkm: int
    TotalUniqueSpecies: int
    TotalPerfectIVs: int
    TotalMaxEVs: int
    TotalShinies: int
    TotalNicknamed: int

    TopBalls: dict[str, int]
    TopHeldItems: dict[str, int]
    TopMoves: dict[str, dict[str, str | int]]
    TopMoveTypes: dict[str, int]
    TopPkms: dict[int, dict[str, str | int]]
    TopPkmTypes: dict[str, int]


class SaveStats(BaseModel):
    TotalSaves: int
    TotalPlayedSeconds: int
    TotalMoney: int

    # TopVersions: dict[str, int]


class StatQuery(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    isShiny: Optional[bool] = False
    saveID: Optional[str] = None


class PkmQuery(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    isShiny: Optional[bool] = False
    saveID: Optional[str] = None
    page: Optional[int] = 0
    pageSize: Optional[int] = 30


class Species(BaseModel):
    Sprite: str


class Pkm(BaseModel):
    ID: int

    Species: str
    SpeciesID: int
    Form: str
    FormID: int
    FullSlug: str

    SpeciesInfo: Optional["Species"] = None

    Nickname: str
    Nature: str
    Gender: str
    Ability: str
    Move1: str
    Move2: str
    Move3: str
    Move4: str
    HeldItem: str
    HP: str
    ATK: str
    DEF: str
    SPA: str
    SPD: str
    SPE: str
    MetLoc: str
    EggLoc: str
    Ball: str
    OT: str
    Version: str
    OTLang: str
    Legal: str
    EncounterType: str

    PID: str
    IV_HP: int
    IV_ATK: int
    IV_DEF: int
    IV_SPA: int
    IV_SPD: int
    IV_SPE: int
    Level: int
    EV_HP: int
    EV_ATK: int
    EV_DEF: int
    EV_SPA: int
    EV_SPD: int
    EV_SPE: int
    EVTotal: int
    IVTotal: int
    IsShiny: bool
    IsNicknamed: bool
    Friendship: int
    MetYear: int
    MetMonth: int
    MetDay: int

    SaveID: str


TYPES = {
    "normal": 1,
    "fighting": 2,
    "flying": 3,
    "poison": 4,
    "ground": 5,
    "rock": 6,
    "bug": 7,
    "ghost": 8,
    "steel": 9,
    "fire": 10,
    "water": 11,
    "grass": 12,
    "electric": 13,
    "psychic": 14,
    "ice": 15,
    "dragon": 16,
    "dark": 17,
    "fairy": 18,
    "stellar": 19,
    "unknown": 10001,
    "shadow": 10002,
}
