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
    TopMoves: dict[str, int]
    # TopMoveTypes: list[str, int]
    TopPkms: dict[int, dict[str, str | int]]
    # TopPkmTypes: list[str, int]


class SaveStats(BaseModel):
    TotalSaves: int
    TotalPlayedSeconds: int
    TotalMoney: int

    # TopVersions: dict[str, int]


class StatFilter(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    saveID: Optional[str] = None


class PkmFilter(BaseModel):
    evTotal: Optional[int] = 0
    isNicknamed: Optional[bool] = False
    saveID: Optional[str] = None
    page: Optional[int] = 0
    pageSize: Optional[int] = 30
