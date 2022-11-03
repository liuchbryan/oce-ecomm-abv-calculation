from datetime import datetime

from oce_ecomm_abv_calculation.sample_statistics.vanilla import VanillaSampleStatistics
from ..artifacts.sample_df import sample_customer_order_df


class TestInit:
    def test_can_take_named_default_datasets_and_populate_dataset_name(self):
        # Loading this should not throw any exceptions
        # Using Olist Brazilian e-Commerce dataset, which is smaller
        named_dataset = (
            VanillaSampleStatistics(
                dataset="olist_brazilian_ecommerce_customer_order_view",
                response_col='r_BasketValue',
            )
        )

        assert named_dataset.dataset_name == "olist_brazilian_ecommerce_customer_order_view"

    def test_populates_dataset_name_as_custom_for_user_supplied_dataframes(self):
        custom_dataset = (
            VanillaSampleStatistics(
                dataset=sample_customer_order_df,
                response_col='r_response',
            )
        )

        assert custom_dataset.dataset_name == "custom"

    def test_filters_df_between_start_and_end_date(self):
        my_object = VanillaSampleStatistics(
            dataset=sample_customer_order_df,
            response_col='r_response',
            start_time=datetime(2022, 1, 2),
            end_time=datetime(2022, 1, 3)
        )

        print(my_object)

        # Only the three rows on 2022-01-02 would be included (start is inclusive, end is exclusive)
        assert my_object.dataset.shape[0] == 3
