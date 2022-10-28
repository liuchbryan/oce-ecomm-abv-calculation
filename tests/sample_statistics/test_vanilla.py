from datetime import datetime

import pydantic.error_wrappers
import pytest
from oce_ecomm_abv_calculation.sample_statistics.vanilla import VanillaSampleStatistics
from ..artifacts.sample_df import only_event_received_time_df, sample_customer_order_df


class TestInit:
    def test_throws_validation_error_if_required_columns_are_missing(self):
        # Comes only with `EventReceivedTime`, missing e.g. `r_response`
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            VanillaSampleStatistics(
                dataset=only_event_received_time_df,
                response_col='r_response'
            )

        # response_col not in dataframe
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            VanillaSampleStatistics(
                dataset=sample_customer_order_df,
                response_col='r_not_the_response_column'
            )

        # This one is valid and should not raise any error
        VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response',
            start_time=datetime(2022, 1, 2),
            end_time=datetime(2022, 1, 3)
        )


class TestMean:
    def test_returns_expected_mean(self):
        my_object = VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response'
        )
        assert my_object.mean() == pytest.approx(4.85, abs=0.01)


class TestVariance:
    def test_returns_expected_variance(self):
        my_object = VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response'
        )
        assert my_object.variance() == pytest.approx(9.14, abs=0.01)


class TestStandardError:
    def test_returns_expected_standard_error(self):
        my_object = VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response'
        )
        assert my_object.standard_error() == pytest.approx(1.14, abs=0.01)


class TestCount:
    def test_returns_expected_count(self):
        my_object = VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response'
        )
        assert my_object.count() == 7
