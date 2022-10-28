import os

from oce_ecomm_abv_calculation.datasets.uci_online_retail_ii import UCIOnlineRetailIIDataset


class TestInit:
    def test_default_path_should_point_to_data_folder(self):
        assert(
            os.path.samefile(
                UCIOnlineRetailIIDataset.__init__.__defaults__[0],
                f"{os.path.dirname(__file__)}/../../data/online_retail_II.xlsx"
            )
        )

    def test_download_raw_dataset_if_not_already_exist(self):
        target_path = f"{os.path.dirname(__file__)}/../artifacts/online_retail_II.xlsx"
        if os.path.exists(target_path):
            os.remove(target_path)
        assert not os.path.exists(target_path)

        UCIOnlineRetailIIDataset(path=target_path)

        assert os.path.exists(target_path)

    def test_loads_df_member_var(self):
        my_dataset = UCIOnlineRetailIIDataset()
        assert my_dataset.df is not None
        assert my_dataset.df.shape[0] > 1000000
