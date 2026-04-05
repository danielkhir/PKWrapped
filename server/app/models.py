from sqlmodel import Column, Field, SQLModel, String

# class Species(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     slug: str
#     dexnum: str
#     types: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class PkmBase(SQLModel):
    ID: int

    Species: str
    SpeciesID: int
    Form: str
    FormID: int
    FullSlug: str

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


class Pkm(PkmBase, table=True):
    __tablename__ = "pkms"

    ID: int = Field(primary_key=True)
    SaveID: str = Field(foreign_key="saves.ID", ondelete="cascade")


class SaveBase(SQLModel):
    ID: str
    Version: str
    Generation: int
    Gender: int
    OT: str
    TID: int
    SID: int
    PlayedHours: int
    PlayedMinutes: int
    PlayedSeconds: int
    SecondsToStart: int
    SecondsToFame: int
    Money: int
    SeenCount: int
    CaughtCount: int
    MaxSpeciesID: int
    PercentSeen: float
    PercentCaught: float


class Save(SaveBase, table=True):
    __tablename__ = "saves"
    ID: str = Field(sa_column=Column("ID", String, primary_key=True))


class SaveWithStats(SaveBase):
    TotalPkm: int


class PkmStats(SQLModel):
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


class SaveStats(SQLModel):
    TotalSaves: int
    TotalPlayedSeconds: int
    TotalMoney: int

    # TopVersions: dict[str, int]
