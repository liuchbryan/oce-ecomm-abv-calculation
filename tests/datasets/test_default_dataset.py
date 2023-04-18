from oce_ecomm_abv_calculation.datasets.default_datasets import (
    get_default_dataset_by_name,
    uci_online_retail_ii_customer_order_view,
    olist_brazilian_ecommerce_customer_order_view,
    olist_brazilian_ecommerce_customer_order_item_view
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

    def test_gets_olist_brazilian_ecommerce_customer_order_view(self):
        assert (
            olist_brazilian_ecommerce_customer_order_view().equals(
                get_default_dataset_by_name("olist_brazilian_ecommerce_customer_order")
            )
        )

    def test_gets_olist_brazilian_ecommerce_customer_order_item_view(self):
        assert (
            olist_brazilian_ecommerce_customer_order_item_view().equals(
                get_default_dataset_by_name("olist_brazilian_ecommerce_customer_order_item")
            )
        )

    def test_capitalization_should_not_matter(self):
        assert (
            olist_brazilian_ecommerce_customer_order_view().equals(
                get_default_dataset_by_name("OLIST_brazilian_ecommerce_customer_order")
            )
        )
        assert (
            olist_brazilian_ecommerce_customer_order_view().equals(
                get_default_dataset_by_name("Olist_Brazilian_Ecommerce_Customer_Order")
            )
        )
        assert (
            olist_brazilian_ecommerce_customer_order_view().equals(
                get_default_dataset_by_name("olist_brazilian_ecommerce_cUsToMeR_order")
            )
        )
