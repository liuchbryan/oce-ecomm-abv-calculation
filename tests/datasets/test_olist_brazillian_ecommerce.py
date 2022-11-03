import numpy as np
import os
import pandas as pd
import pytest

from oce_ecomm_abv_calculation.datasets.olist_brazilian_ecommerce import (
    _download_raw_dataset_from_internet, OlistBrazilianEcommerceDataset
)


class TestDownloadRawDatasetFromInternet:
    def test_downloads_file(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        file_name = "olist_customers_dataset.csv"
        target_file_path = os.path.join(target_dir_path, file_name)

        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        _download_raw_dataset_from_internet(target_file_path, file_name)
        assert os.path.exists(target_file_path)

    def test_downloads_file_only_once(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        file_name = "olist_customers_dataset.csv"
        target_file_path = os.path.join(target_dir_path, file_name)

        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        _download_raw_dataset_from_internet(target_file_path, file_name)
        # Duplicate files get a " (1)" appended before the file extension
        assert not os.path.exists(os.path.join(target_dir_path,
                                               "olist_customers_dataset (1).csv"))

    def test_raises_error_if_non_existent_file_name_specified(self):
        out_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        with pytest.raises(RuntimeError):
            _download_raw_dataset_from_internet(out_dir_path, file_name="wrong_file_name.csv")


class TestInit:
    def test_default_path_should_point_to_data_folder(self):
        assert(
            os.path.samefile(
                OlistBrazilianEcommerceDataset.__init__.__defaults__[0],
                f"{os.path.dirname(__file__)}/../../data"
            )
        )

    def test_download_raw_dataset_if_not_already_exist(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        target_file_path = os.path.join(target_dir_path, "olist_customers_dataset.csv")
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        OlistBrazilianEcommerceDataset(path=target_dir_path)

        assert os.path.exists(target_file_path)

    def test_also_takes_file_path_in_addition_to_dir_path(self):
        # See test above for a "load via dir path" unit test
        # The correct behaviour is to ignore the file name (as we have deal with multiple files)
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/olist_customers_dataset.csv"
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        OlistBrazilianEcommerceDataset(path=target_file_path)

        assert os.path.exists(target_file_path)

    def test_loads_df_member_var(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path)

        assert my_dataset.df is not None
        assert my_dataset.df.shape[0] > 100000


class TestCleanDataView:
    def test_filters_out_nan_rows_in_order_customer_product_id(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).clean_data_view()

        assert my_dataset[
            my_dataset["order_id"].isnull() |
            my_dataset["customer_unique_id"].isnull() |
            my_dataset["product_id"].isnull()
        ].shape[0] == 0

    def test_contains_necessary_columns_for_standardized_views(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).clean_data_view()

        assert all(
            required_col in my_dataset.columns
            for required_col in ['order_id',
                                 'customer_unique_id',
                                 'product_id',
                                 'order_purchase_timestamp',
                                 'order_item_id',
                                 'price']
        )


class TestStandardizedCustomerOrderDataView:
    def test_output_has_the_required_columns(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).standardized_customer_order_data_view()

        assert all(
            required_col in my_dataset.columns
            for required_col in ["RandomizationUnitId",
                                 "AnalysisUnitId",
                                 "EventReceivedTime",
                                 "r_BasketValue",
                                 "r_BasketSize"]
        )

    def test_output_are_at_customer_order_level(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).standardized_customer_order_data_view()

        assert my_dataset.shape[0] == my_dataset["AnalysisUnitId"].nunique()

        # The dataset has 99441 unique `order_id`s according to Kaggle
        assert my_dataset.shape[0] <= 99441

        # At least one customer has more than one order
        assert my_dataset.shape[0] > my_dataset["RandomizationUnitId"].nunique()

    def test_event_received_time_col_is_datetime_type(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).standardized_customer_order_data_view()

        assert pd.api.types.is_datetime64_dtype(my_dataset["EventReceivedTime"].dtype)


class TestStandardizedCustomerOrderItemDataView:
    def test_output_has_the_required_columns(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).standardized_customer_order_item_data_view()
        #         RandomizationUnitId: The customer identifier
        #         SecondaryUnitId: The product / stock keeping unit (SKU) identifier
        #         AnalysisUnitId: The identifier for the item within an order
        #                         (often in format of `<order>_<item>`)
        #         EventReceivedTime: The time the order occurred
        #         r_SellingPrice: The price of the item sold
        assert all(
            required_col in my_dataset.columns
            for required_col in ["RandomizationUnitId",
                                 "SecondaryUnitId",
                                 "AnalysisUnitId",
                                 "EventReceivedTime",
                                 "r_SellingPrice"]
        )

    def test_output_are_at_customer_order_item_level(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        my_dataset = OlistBrazilianEcommerceDataset(path=target_dir_path).standardized_customer_order_item_data_view()

        assert my_dataset.shape[0] == my_dataset["AnalysisUnitId"].nunique()

        # At least one order has multiple items involved
        assert my_dataset.shape[0] > my_dataset["order_id"].nunique()
