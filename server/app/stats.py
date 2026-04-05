import pandas as pd

from .models import PkmStats, SaveStats

MAX_EVS = 510
MAX_IVS = 31 * 6


def get_top_n_dict(ser: pd.Series, limit: int = 5):
    return ser.value_counts().head(limit).to_dict()


class StatCalculator:
    def __init__(self, save_df: pd.DataFrame, pkm_df: pd.DataFrame):
        self.save_df = save_df
        self.pkm_df = pkm_df

    def calc_save_stats(self):
        return SaveStats(
            TotalSaves=self.save_df.ID.count(),
            TotalPlayedSeconds=(
                self.save_df.PlayedHours * 3600
                + self.save_df.PlayedMinutes * 60
                + self.save_df.PlayedSeconds
            ).sum(),
            TotalMoney=self.save_df.Money.sum(),
        )

    def calc_pkm_stats(self, limit: int = 5):
        moves = self.pkm_df[["Move1", "Move2", "Move3", "Move4"]].melt(
            value_name="move"
        )
        moves = moves[moves["move"] != "none"]["move"]

        return PkmStats(
            TotalPkm=self.pkm_df.ID.count(),
            TotalUniqueSpecies=self.pkm_df.SpeciesID.nunique(),
            TotalPerfectIVs=self.pkm_df[self.pkm_df.IVTotal == MAX_IVS].ID.count(),
            TotalMaxEVs=self.pkm_df[self.pkm_df.EVTotal == MAX_EVS].ID.count(),
            TotalShinies=self.pkm_df[self.pkm_df.IsShiny == 1].ID.count(),
            TotalNicknamed=self.pkm_df[self.pkm_df.IsNicknamed == 1].ID.count(),
            TopBalls=get_top_n_dict(self.pkm_df.Ball, limit),
            TopMoves=get_top_n_dict(moves, limit),
            TopPkms=get_top_n_dict(self.pkm_df.Species),
        )
