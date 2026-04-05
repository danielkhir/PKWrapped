import sqlite3
from typing import Annotated

import pandas as pd
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DB_PATH = "../data/db.sqlite"

db_url = f"sqlite:///{DB_PATH}"
connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def read_tables():
    con = sqlite3.connect(DB_PATH)
    save_df = pd.read_sql_query("SELECT * from saves", con)
    pkm_df = pd.read_sql_query("SELECT * from pkms", con)
    con.close()
    return save_df, pkm_df


SessionDep = Annotated[Session, Depends(get_session)]
