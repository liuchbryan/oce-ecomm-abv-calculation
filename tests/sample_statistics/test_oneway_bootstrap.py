from datetime import datetime

import pydantic.error_wrappers
import pytest
from oce_ecomm_abv_calculation.sample_statistics.oneway_bootstrap import OnewayBootstrapStatistics
from ..artifacts.sample_df import only_event_received_time_df, sample_customer_order_df


class TestInit:
    def test_throws_validation_error_if_required_columns_are_missing(self):
        # Comes only with `EventReceivedTime`, missing e.g. `r_response`
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            OnewayBootstrapStatistics(
                dataset=only_event_received_time_df,
                response_col='r_response'
            )

        # response_col not in dataframe
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            OnewayBootstrapStatistics(
                dataset=sample_customer_order_df,
                response_col='r_not_the_response_column'
            )

        # This one is valid and should not raise any error
        OnewayBootstrapStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response',
            start_time=datetime(2022, 1, 2),
            end_time=datetime(2022, 1, 3)
        )


class TestMean:
    def test_successive_calls_returns_non_deterministic_values(self):
        # Two bootstrap means are most likely to be different form each other
        oneway_bootstrap = (
            OnewayBootstrapStatistics(
                dataset=sample_customer_order_df,
                response_col='r_response'
            )
        )
        try:
            assert oneway_bootstrap.mean() != oneway_bootstrap.mean()
        except AssertionError:
            # Try again if two successive calls happen to return the same mean (which happens)
            assert oneway_bootstrap.mean() != oneway_bootstrap.mean()

    def test_populates_latest_mean_class_variable(self):
        oneway_bootstrap = (
            OnewayBootstrapStatistics(
                dataset=sample_customer_order_df,
                response_col='r_response'
            )
        )
        expected_mean = oneway_bootstrap.mean()
        assert oneway_bootstrap.latest_mean == expected_mean


class TestCount:
    def test_returns_expected_count(self):
        my_object = OnewayBootstrapStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response'
        )
        print(my_object)

        assert my_object.count() == 7
