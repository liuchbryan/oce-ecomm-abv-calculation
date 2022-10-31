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
