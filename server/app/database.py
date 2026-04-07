import os
import sqlite3

import pandas as pd
from sqlmodel import Session, SQLModel, create_engine

from .models import StatFilter

DB_PATH = os.getenv("PKW_DB_URL", "./data/test.sqlite")

db_url = f"sqlite:///{DB_PATH}"
connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def read_tables(stat_filter: StatFilter):
    con = sqlite3.connect(DB_PATH)
    save_stmt = "SELECT * from saves"
    pkm_stmt = "SELECT * from pkms"
    spc_stmt = "SELECT * from species"
    move_stmt = "SELECT * from move"

    pkm_stmt += f" WHERE EVTotal >= {stat_filter.evTotal}"

    if stat_filter.isNicknamed:
        pkm_stmt += " AND IsNicknamed == True"
    if stat_filter.isShiny:
        pkm_stmt += " AND IsShiny == True"
    if stat_filter.saveID:
        save_stmt += f" WHERE ID == '{stat_filter.saveID}'"
        pkm_stmt += f" AND SaveID == '{stat_filter.saveID}'"

    save_df = pd.read_sql_query(save_stmt, con)
    pkm_df = pd.read_sql_query(pkm_stmt, con)
    spc_df = pd.read_sql_query(spc_stmt, con)
    move_df = pd.read_sql_query(move_stmt, con)

    con.close()
    return save_df, pkm_df, spc_df, move_df


def truncate_tables():
    return [
        "delete from saves;",
        "delete from sqlite_sequence where name='saves';",
        "delete from pkms;",
        "delete from sqlite_sequence where name='pkmns';",
    ]
