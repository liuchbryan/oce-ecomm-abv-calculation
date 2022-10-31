from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, validator, root_validator
from typing import Union

from ..datasets.default_datasets import get_default_dataset_by_name


class SampleStatistics(ABC, BaseModel):
    response_col: str
    start_time: datetime = datetime(1970, 1, 1)
    end_time: datetime = datetime(2100, 1, 1)

    dataset_name: str = None
    dataset: Union[pd.DataFrame, str]

    class Config:
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def set_dataset_name(cls, values) -> str:
        if isinstance(values["dataset"], str):
            values['dataset_name'] = values["dataset"]
        else:
            values['dataset_name'] = "custom"
        return values

    @validator('dataset')
    def get_dataset(cls, candidate_dataset, values) -> pd.DataFrame:
        if isinstance(candidate_dataset, str):
            df = get_default_dataset_by_name(candidate_dataset)
        else:
            df = candidate_dataset

        if df is None:
            raise ValueError("No dataframe loaded. This may be due to an invalid default"
                             "dataset name or an None being passed to the `dataset` argument.")

        assert "EventReceivedTime" in df.columns, "Dataset must contain the column `EventReceivedTime`."
        assert values["response_col"] in df.columns, f"Dataset must contain the column `{values['response_col']}`."

        return(
            df[
                (values["start_time"] <= df["EventReceivedTime"]) &
                (df["EventReceivedTime"] < values["end_time"])
            ]
        )

    @abstractmethod
    def mean(self):
        pass

    @abstractmethod
    def variance(self):
        pass

    @abstractmethod
    def standard_error(self):
        pass

    @abstractmethod
    def count(self):
        pass
