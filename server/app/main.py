import subprocess

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, File, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, func, select, text

from .database import get_session, create_db_and_tables, read_tables, truncate_tables
from .models import Pkm, Save, SaveWithStats, StatFilter, PkmFilter, PkmWithSpecies
from .stats import StatCalculator


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/stats/", response_model=list)
def calc_saves(stat_filter: Annotated[StatFilter, Query()]):
    save_df, pkm_df, spc_df, move_df = read_tables(stat_filter)

    calc = StatCalculator(save_df, pkm_df, spc_df, move_df)

    save_stats = calc.calc_save_stats()
    pkm_stats = calc.calc_pkm_stats()
    return [save_stats, pkm_stats]


@app.get("/saves/", response_model=list[Save])
def read_saves(session: SessionDep):
    return session.exec(select(Save)).all()


@app.post("/saves/", response_model=str)
def post_saves(file: Annotated[bytes, File()]):
    with open("./data/temp.sav", "wb") as f:
        f.write(file)

    subprocess.run(["./PKBridge", "-i", "./data/temp.sav", "-o", "./data/"])

    return "OK"


@app.delete("/saves/", response_model=str)
def delete_saves(session: SessionDep):
    for stmt in truncate_tables():
        session.exec(text(stmt))
    session.commit()
    return "OK"


@app.get("/saves/{save_id}/", response_model=SaveWithStats)
def read_save(save_id: str, session: SessionDep):
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail="Run not found")

    stmt = select(func.count(Pkm.ID)).where(Pkm.SaveID == save_id)
    total_pkm = session.exec(stmt).one()

    save_with_stats = SaveWithStats(
        **save.model_dump(),
        TotalPkm=total_pkm,
    )
    return save_with_stats


@app.get("/pkms/", response_model=list[PkmWithSpecies])
def read_pkms(
    session: SessionDep,
    pkm_filter: Annotated[PkmFilter, Query()],
):
    stmt = select(Pkm)

    if pkm_filter.saveID:
        stmt = stmt.where(Pkm.SaveID == pkm_filter.saveID)
    if pkm_filter.evTotal:
        stmt = stmt.where(Pkm.EVTotal == pkm_filter.evTotal)
    if pkm_filter.isNicknamed:
        stmt = stmt.where(Pkm.IsNicknamed == pkm_filter.isNicknamed)
    if pkm_filter.isShiny:
        stmt = stmt.where(Pkm.IsShiny == pkm_filter.isShiny)

    # stmt = stmt.join(Species, Species.FormName == Pkm.FullSlug, isouter=True)

    stmt = stmt.limit(pkm_filter.pageSize)
    stmt = stmt.offset(pkm_filter.page * pkm_filter.pageSize)

    pkms = session.exec(stmt).all()
    return pkms


@app.get("/pkms/random/", response_model=list[int])
def read_random(
    session: SessionDep,
):
    stmt = (
        select(Pkm.SpeciesID)
        .where(Pkm.EVTotal >= 100)
        .order_by(func.random())
        .limit(30)
    )
    ids = session.exec(stmt).all()
    return ids


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
