from .sample_statistics import SampleStatistics
from pydantic import BaseModel, validator


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
