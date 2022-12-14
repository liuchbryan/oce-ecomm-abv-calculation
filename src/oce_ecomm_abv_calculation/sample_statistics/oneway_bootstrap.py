import numpy as np
import pandas as pd
import os
from pydantic import validator
import time
from typing import List

from .sample_statistics import SampleStatistics

COL_RANDOMIZATION_UNIT_ID = "RandomizationUnitId"
COL_ANALYSIS_UNIT_ID = "AnalysisUnitId"


class OnewayBootstrapStatistics(SampleStatistics):

    # Some fields to enable saving the output
    latest_mean: float = None
    # List of bootstrap means to calculate the bootstrap standard error (by taking the standard deviation)
    latest_means: List[float] = None
    latest_standard_error: float = None

    @validator('dataset')
    def check_column_name_exists(cls, candidate_dataset) -> pd.DataFrame:
        assert (
                (COL_ANALYSIS_UNIT_ID in candidate_dataset.columns) and
                (COL_RANDOMIZATION_UNIT_ID in candidate_dataset.columns)
        ), \
            f"Dataset must contain the column {COL_RANDOMIZATION_UNIT_ID} and {COL_ANALYSIS_UNIT_ID}."
        return candidate_dataset

    @validator('latest_mean', pre=True, always=True)
    def set_latest_mean_to_none(cls, _) -> None:
        return None

    @validator('latest_means', pre=True, always=True)
    def set_latest_means_to_empty_list(cls, _) -> List[float]:
        return []

    @validator('latest_standard_error', pre=True, always=True)
    def set_latest_standard_error_to_none(cls, _) -> None:
        return None

    def mean(self) -> float:
        """
        Generate one one-way bootstrap sample mean of `response_col`. This is done by
        (1) Resampling `dataset` where each `RandomizationUnitId` gets the same Poisson(1) weight, and
        (2) Calculating the sample mean (over all `AnalysisUnitId`s) of the resample.
        The function also updates the `latest_mean` class variable.
        :return: Sample mean of a one-way bootstrap resample
        """
        sum_weight_df = (
                self.dataset
                .groupby(COL_RANDOMIZATION_UNIT_ID)
                .agg(
                    response_sum=pd.NamedAgg(column=self.response_col, aggfunc="sum"),
                    response_count=pd.NamedAgg(column=COL_ANALYSIS_UNIT_ID, aggfunc="nunique"),
                    weight=pd.NamedAgg(column=COL_ANALYSIS_UNIT_ID,
                                       aggfunc=lambda does_not_matter: np.random.default_rng().poisson(lam=1.0)),
                )
                .reset_index()
        )

        sum_weighted_sum = np.sum(sum_weight_df["response_sum"] * sum_weight_df["weight"])
        count_weighted_sum = np.sum(sum_weight_df["response_count"] * sum_weight_df["weight"])

        self.latest_mean = sum_weighted_sum / count_weighted_sum

        return self.latest_mean

    def standard_error(self, num_bootstrap_means: int = 100, verbose=False) -> float:
        """
        Generate one one-way bootstrap standard error of `response_col`. This is done by
        (1) Generate `num_bootsrap_means` bootstrap means
        (2) Calculate the standard _deviation_ of the bootstrap means
        The function also updates the `latest_means` and `latest_standard_error` variables.
        :param num_bootstrap_means: Number of bootstrap means used to calculated the sample standard error
        :param verbose: If true, prints the current progress in roughly 1% increments.
        :return: One sample standard error from many bootstrap mean samples
        """
        self.latest_means = []
        last_reported_iter = 0
        for curr_iter in range(1, num_bootstrap_means + 1):
            if verbose and ((curr_iter - last_reported_iter) >= num_bootstrap_means / 100):
                last_reported_iter = curr_iter
                print(f"Calculating bootstrap mean {curr_iter}/{num_bootstrap_means}...", end="\r")

            self.latest_means.append(self.mean())

        self.latest_standard_error = np.std(self.latest_means)

        return self.latest_standard_error

    def variance(self, num_bootstrap_means: int = 100) -> float:
        """
        Generate one one-way bootstrap sample variance of `response_col`. This is done by getting a bootstrap standard
        error (generating a fresh one if none already exists), square it, and multiply the result by the sample count.
        :param num_bootstrap_means: Number of bootstrap means used to calculated the sample standard error
        :return:
        """
        if self.latest_standard_error is not None:
            se = self.latest_standard_error
        else:
            se = self.standard_error(num_bootstrap_means=num_bootstrap_means, verbose=False)

        return se ** 2 * self.count()

    def count(self) -> int:
        return self.dataset["AnalysisUnitId"].nunique()

    def save_latest_result_as_pd_df(self, path=None) -> None:
        results_df = (
            pd.DataFrame([
                {"dataset_name": self.dataset_name,
                 "response_col": self.response_col,
                 "start_time": self.start_time,
                 "end_time": self.end_time,
                 "num_bootstrap_means": len(self.latest_means),
                 "bootstrap_mean": self.latest_mean,
                 "bootstrap_means": self.latest_means,
                 "bootstrap_standard_error": self.latest_standard_error,
                 "count": self.count()}
            ])
        )

        if path is None:
            output_path = (
                f"{os.path.dirname(__file__)}/../../../data/" +
                "_".join([
                    "expt",
                    "oneway",
                    self.dataset_name.replace("_", "-"),
                    self.response_col.replace("_", "-"),
                    str(int(time.time()))
                ]) +
                ".parquet"
            )
        else:
            output_path = path

        results_df.to_parquet(output_path)
