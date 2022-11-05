import glob
import os
import pandas as pd
import shutil
from oce_ecomm_abv_calculation.utils.experiment_data import consolidate_experiment_data_files


class TestConsolidateExperimentDataFiles:
    def test_consolidate_files(self):
        expected_out_file_path = (
            f"{os.path.dirname(__file__)}/../artifacts/"
            "expt_oneway_olist-brazilian-ecommerce-customer-order-item-view_r-SellingPrice_consolidated.parquet")
        if os.path.exists(expected_out_file_path):
            os.remove(expected_out_file_path)
        assert not os.path.exists(expected_out_file_path)

        actual_out_file_path = (
            consolidate_experiment_data_files(
                dir_path=f"{os.path.dirname(__file__)}/../artifacts/",
                expt_method="oneway",
                dataset="olist_brazilian_ecommerce_customer_order_item_view",
                response_col="r_SellingPrice",
                cleanup_files=False
            )
        )

        assert actual_out_file_path == expected_out_file_path
        assert os.path.exists(actual_out_file_path)
        assert pd.read_parquet(actual_out_file_path).shape[0] == 2

    def test_can_clean_up_pre_consolidation_files(self):
        dir_path = f"{os.path.dirname(__file__)}/../artifacts/"

        # Remove the expected output file if exist
        expected_out_file_path = (
            dir_path +
            "expt_oneway_olist-brazilian-ecommerce-customer-order-item-view_r-SellingPrice_consolidated.parquet")
        if os.path.exists(expected_out_file_path):
            os.remove(expected_out_file_path)
        assert not os.path.exists(expected_out_file_path)

        # Create a temp storage for existing experiment data files so we can restore them later
        temp_dir_path = os.path.join(dir_path, "temp")
        os.mkdir(temp_dir_path)
        existing_experiment_data_files = glob.glob(os.path.join(dir_path, "expt_oneway_olist*.parquet"))
        for file in existing_experiment_data_files:
            shutil.copy(file, os.path.join(temp_dir_path, os.path.basename(file)))

        consolidate_experiment_data_files(
            dir_path=dir_path,
            expt_method="oneway",
            dataset="olist_brazilian_ecommerce_customer_order_item_view",
            response_col="r_SellingPrice",
            cleanup_files=True
        )

        for file in existing_experiment_data_files:
            assert not os.path.exists(file)

        # Restore experiment data files from temp storage
        for file in existing_experiment_data_files:
            os.rename(os.path.join(temp_dir_path, os.path.basename(file)), file)
        os.rmdir(temp_dir_path)

    def test_ignore_duplicate_experiment_data_entries(self):
        expected_out_file_path = (
            f"{os.path.dirname(__file__)}/../artifacts/"
            "expt_oneway_olist-brazilian-ecommerce-customer-order-item-view_r-SellingPrice_consolidated.parquet")
        if os.path.exists(expected_out_file_path):
            os.remove(expected_out_file_path)
        assert not os.path.exists(expected_out_file_path)

        # Generates a consolidated file with the source files intact
        consolidate_experiment_data_files(
            dir_path=f"{os.path.dirname(__file__)}/../artifacts/",
            expt_method="oneway",
            dataset="olist_brazilian_ecommerce_customer_order_item_view",
            response_col="r_SellingPrice",
            cleanup_files=False
        )

        # Now the consolidated file will also be read as an experiment file, which will
        # duplicate the experiment data if things are not handled properly
        actual_out_file_path = consolidate_experiment_data_files(
            dir_path=f"{os.path.dirname(__file__)}/../artifacts/",
            expt_method="oneway",
            dataset="olist_brazilian_ecommerce_customer_order_item_view",
            response_col="r_SellingPrice",
            cleanup_files=False
        )

        assert pd.read_parquet(actual_out_file_path).shape[0] == 2
