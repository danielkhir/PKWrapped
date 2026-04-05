from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import func, select

from .database import SessionDep, create_db_and_tables, read_tables
from .models import Pkm, Save, SaveWithStats
from .stats import StatCalculator


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


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


@app.get("/saves/", response_model=list[Save])
def read_saves(session: SessionDep):
    return session.exec(select(Save)).all()


@app.get("/stats/", response_model=list)
def calc_saves(session: SessionDep):
    save_df, pkm_df = read_tables()

    calc = StatCalculator(save_df, pkm_df)

    save_stats = calc.calc_save_stats()
    pkm_stats = calc.calc_pkm_stats()
    return [save_stats, pkm_stats]


@app.get("/saves/{save_id}", response_model=SaveWithStats)
def read_save(save_id: str, session: SessionDep):
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail="Run not found")

    total_pkm = session.exec(
        select(func.count(Pkm.ID)).where(Pkm.SaveID == save_id)
    ).one()

    save_with_stats = SaveWithStats(
        **save.model_dump(),
        TotalPkm=total_pkm,
    )
    return save_with_stats


@app.get("/pkms/", response_model=list[Pkm])
def read_pkms(
    session: SessionDep,
    save_id: str | None = None,
    page: int | None = None,
    page_size: int = 30,
):
    stmt = select(Pkm)
    if save_id:
        stmt = stmt.where(Pkm.SaveID == save_id)
    if page_size:
        stmt = stmt.limit(page_size)
    if page:
        stmt = stmt.offset(page * page_size)
    pkms = session.exec(stmt).all()
    return pkms


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
