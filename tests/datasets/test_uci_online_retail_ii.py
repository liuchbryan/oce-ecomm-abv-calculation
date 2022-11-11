import os

from oce_ecomm_abv_calculation.datasets.uci_online_retail_ii import UCIOnlineRetailIIDataset


class TestInit:
    def test_default_path_should_point_to_data_folder(self):
        assert(
            os.path.samefile(
                UCIOnlineRetailIIDataset.__init__.__defaults__[0],
                f"{os.path.dirname(__file__)}/../../data"
            )
        )

    def test_download_raw_dataset_if_not_already_exist(self):
        target_dir_path = f"{os.path.dirname(__file__)}/../artifacts"
        target_file_path = os.path.join(target_dir_path, "online_retail_II.xlsx")
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        UCIOnlineRetailIIDataset(path=target_dir_path)

        assert os.path.exists(target_file_path)

    def test_also_takes_file_path_in_addition_to_dir_path(self):
        # See test above for a "load via dir path" unit test
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        assert not os.path.exists(target_file_path)

        UCIOnlineRetailIIDataset(path=target_file_path)

        assert os.path.exists(target_file_path)

    def test_loads_df_member_var(self):
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        my_dataset = UCIOnlineRetailIIDataset(path=target_file_path)

        assert my_dataset.df is not None
        assert my_dataset.df.shape[0] > 1000000


class TestCleanDataView:
    def test_output_has_unique_key_as_invoice_stockcode_price(self):
        # The same (Invoice, StockCode, Price) can appear in multiple rows.
        # Think of your receipt when buying multiple units of the same product in the supermarket, the units are
        # sometimes combined, sometimes listed as separated entries, and sometimes have another product in between.
        # In addition, same (Invoice, StockCode, Price) can have different `InvoiceDate`, and `Description`. This
        # is likely a data issue, but needs to be taken into account when generating various views.
        # This test ensures we at least have a unique key (as (Invoice, StockCode, Price) in the clean data view.
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        my_dataset = UCIOnlineRetailIIDataset(path=target_file_path).clean_data_view()

        assert(
            my_dataset.drop_duplicates(
                subset=["Invoice", "StockCode", "Price"]).shape[0] ==
            my_dataset.shape[0]
        )

    def test_output_adds_subtotal_columns(self):
        # The price column refers to the price per unit - it would be easier to have a running total
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        my_dataset = UCIOnlineRetailIIDataset(path=target_file_path).clean_data_view()

        assert "Subtotal" in my_dataset.columns


class TestStandardizedCustomerOrderDataView:
    def test_output_has_the_required_columns(self):
        target_file_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        my_dataset = UCIOnlineRetailIIDataset(path=target_file_path).standardized_customer_order_data_view()

        assert all(
            required_col in my_dataset.columns
            for required_col in ["RandomizationUnitId",
                                 "AnalysisUnitId",
                                 "EventReceivedTime",
                                 "r_BasketValue",
                                 "r_BasketSize"]
        )
