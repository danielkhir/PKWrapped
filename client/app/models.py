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


class StatFilter(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    isShiny: Optional[bool] = False
    saveID: Optional[str] = None


class PkmFilter(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    isShiny: Optional[bool] = False
    saveID: Optional[str] = None
    page: Optional[int] = 0
    pageSize: Optional[int] = 30


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
