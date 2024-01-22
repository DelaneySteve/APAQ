"""
    Class used to prepare the user data, 
    load a trained model, and make a prediction. 
"""

import pickle
import pandas as pd
from sklearn.ensemble import BaseEnsemble #type: ignore [import-untyped]
from data.stats.get_runway_stats import RunwayStats

class Model:
    def __init__(self) -> None:
        self._model = None #type: BaseEnsemble

    def load_trained_model(self, filename: str) -> None:
        with open(filename, "rb") as f:
            model = pickle.load(f)
        self._model = model

    def _input_prep(self, user_input: pd.DataFrame) -> pd.DataFrame:
        runways_input = user_input[["runways"]]
        runways_stats_df = RunwayStats(runways_input).runway_df()
        input_df = pd.concat([user_input.drop(["runways"],axis = 1),runways_stats_df], axis= 1)
        return input_df[["altitude","runways","total_runway_length","arrivals","departures"]]

    def predict(self, user_input: pd.DataFrame) -> int:
        prepped_input = self._input_prep(user_input)
        return self._model.predict(prepped_input)
