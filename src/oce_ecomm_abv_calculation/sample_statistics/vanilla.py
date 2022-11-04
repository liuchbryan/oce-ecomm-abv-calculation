import os
import pandas as pd
from pydantic import BaseModel, validator
import time

from .sample_statistics import SampleStatistics


class VanillaSampleStatistics(SampleStatistics, BaseModel):

    @validator('dataset')
    def check_column_name_exists(cls, candidate_dataset):
        assert "AnalysisUnitId" in candidate_dataset.columns, \
            "Dataset must contain the column `AnalysisUnitId`."
        return candidate_dataset

    def mean(self):
        return self.dataset[self.response_col].mean()

    def variance(self):
        return self.dataset[self.response_col].var()

    def standard_error(self):
        return self.dataset[self.response_col].sem()

    def count(self):
        return self.dataset["AnalysisUnitId"].nunique()

    def save_latest_result_as_pd_df(self, path=None) -> None:
        results_df = (
            pd.DataFrame([
                {"dataset_name": self.dataset_name,
                 "response_col": self.response_col,
                 "start_time": self.start_time,
                 "end_time": self.end_time,
                 "sample_mean": self.mean(),
                 "sample_standard_error": self.standard_error(),
                 "sample_variance": self.variance(),
                 "count": self.count()}
            ])
        )

        if path is None:
            output_path = (
                f"{os.path.dirname(__file__)}/../../../data/" +
                "_".join([
                    "expt",
                    "vanilla",
                    self.dataset_name.replace("_", "-"),
                    self.response_col.replace("_", "-"),
                    str(int(time.time()))
                ]) +
                ".parquet"
            )
        else:
            output_path = path

        results_df.to_parquet(output_path)
