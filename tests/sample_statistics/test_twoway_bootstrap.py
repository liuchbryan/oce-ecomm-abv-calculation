from datetime import datetime
import os
import pandas as pd
import pydantic.error_wrappers
import pytest
from oce_ecomm_abv_calculation.sample_statistics.twoway_bootstrap import TwowayBootstrapStatistics
from ..artifacts.sample_df import only_event_received_time_df, sample_customer_order_df, sample_customer_order_item_df


class TestInit:
    def test_throws_validation_error_if_required_columns_are_missing(self):
        # Comes only with `EventReceivedTime`, missing e.g. `r_response`
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            TwowayBootstrapStatistics(
                dataset=only_event_received_time_df,
                response_col='r_response'
            )

        # SecondaryUnitId missing
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_df,
                response_col='r_response'
            )

        # response_col not in dataframe
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_not_the_response_column'
            )

        # This one is valid and should not raise any error
        TwowayBootstrapStatistics(
            dataset=sample_customer_order_item_df,
            response_col='r_response',
            start_time=datetime(2022, 1, 2),
            end_time=datetime(2022, 1, 3)
        )


class TestMean:
    def test_successive_calls_returns_non_deterministic_values(self):
        # Two bootstrap means are most likely to be different form each other
        # This one test two successive `mean()` calls (i.e., taking the first and second bootstrap mean)
        twoway_bootstrap = (
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_response'
            )
        )
        try:
            assert twoway_bootstrap.mean() != twoway_bootstrap.mean()
        except AssertionError:
            # Try again if two successive calls happen to return the same mean (which happens)
            assert twoway_bootstrap.mean() != twoway_bootstrap.mean()

    def test_different_object_returns_non_deterministic_values(self):
        # Two bootstrap means are most likely to be different form each other
        # This one test calls to two different objects (both taking the first bootstrap mean)
        twoway_bootstrap_1 = (
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_response'
            )
        )
        twoway_bootstrap_2 = (
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_response'
            )
        )
        try:
            assert twoway_bootstrap_1.mean() != twoway_bootstrap_2.mean()
        except AssertionError:
            # Try again if two objects happen to return the same mean (which happens)
            assert twoway_bootstrap_1.mean() != twoway_bootstrap_2.mean()

    def test_populates_latest_mean_class_variable(self):
        twoway_bootstrap = (
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_response'
            )
        )
        expected_mean = twoway_bootstrap.mean()
        assert twoway_bootstrap.latest_mean == expected_mean


class TestCount:
    def test_returns_expected_count(self):
        my_object = TwowayBootstrapStatistics(
            dataset=sample_customer_order_item_df,
            response_col='r_response'
        )

        assert my_object.count() == 13


class TestSaveLatestResultAsPdDf:
    def test_saves_valid_results(self):
        # An E2E test
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        target_file_path = os.path.join(target_dir_path, "expt_twoway_test.parquet")

        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        twoway_bootstrap = (
            TwowayBootstrapStatistics(
                dataset=sample_customer_order_item_df,
                response_col='r_response',
                start_time=datetime(2022, 1, 1),
                end_time=datetime(2022, 1, 5)
            )
        )
        twoway_bootstrap.standard_error(num_bootstrap_means=10)
        twoway_bootstrap.save_latest_result_as_pd_df(path=target_file_path)

        assert os.path.exists(target_file_path)

        twoway_statistics_df = pd.read_parquet(target_file_path)
        assert([
            col in twoway_statistics_df.columns
            for col in [
                'dataset_name',
                'response_col',
                'start_time',
                'end_time',
                'num_bootstrap_means',
                'bootstrap_mean',
                'bootstrap_means',
                'bootstrap_standard_error',
                'count'
            ]
        ])
        assert(twoway_statistics_df.shape[0] == 1)
        assert(twoway_statistics_df['response_col'].iloc[0] == 'r_response')
        assert(twoway_statistics_df['start_time'].iloc[0] == datetime(2022, 1, 1))
        assert(twoway_statistics_df['end_time'].iloc[0] == datetime(2022, 1, 5))
        assert(twoway_statistics_df['num_bootstrap_means'].iloc[0] == 10)
        assert(twoway_statistics_df['bootstrap_means'].iloc[0].shape[0] == 10)
