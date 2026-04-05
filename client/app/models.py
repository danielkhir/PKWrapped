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
    TopPkms: dict[str, int]
    # TopPkmTypes: list[str, int]


class SaveStats(BaseModel):
    TotalSaves: int
    TotalPlayedSeconds: int
    TotalMoney: int

    # TopVersions: dict[str, int]
