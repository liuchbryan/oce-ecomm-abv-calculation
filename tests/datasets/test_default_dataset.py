import pandas as pd
from oce_ecomm_abv_calculation.datasets.default_datasets import (
    get_default_dataset_by_name, uci_online_retail_ii_customer_order_view
)


class TestGetDefaultDatasetByName:
    def test_none_dataset_name_returns_none(self):
        assert get_default_dataset_by_name(None) is None

    def test_gets_uci_online_retail_ii_customer_order_view(self):
        assert(
            uci_online_retail_ii_customer_order_view().equals(
                get_default_dataset_by_name("UCI_Online_Retail_II_Customer_Order")
            )
        )
