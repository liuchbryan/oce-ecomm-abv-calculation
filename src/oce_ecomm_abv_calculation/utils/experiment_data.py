import glob
import os
import pandas as pd
from typing import Optional


def consolidate_experiment_data_files(
    dir_path: str = f"{os.path.dirname(__file__)}/../../../data/",
    expt_method: str = "vanilla",
    dataset: str = "olist_brazilian_ecommerce_customer_order_view",
    response_col: str = "r_BasketValue",
    cleanup_files: bool = False,
) -> Optional[str]:
    """
    :param dir_path: Path of the directory that contains the files to be consolidated
    :param expt_method: e.g. `vanilla` or `oneway`
    :param dataset: Name of the dataset (including specific view) e.g. `olist_brazilian_ecommerce_customer_order_view`
    :param response_col: Name of the response column e.g. `r_BasketValue`
    :param cleanup_files: If the pre-consolidation files should be removed, default `False`.
    :return: The file path of the consolidated experiment data file, if the operation is successful
    """
    path_match_string = (
        "*".join([
            dir_path,
            "expt",
            expt_method,
            dataset.replace("_", "-"),
            response_col.replace("_", "-"),
            ".parquet"
        ])
    )
    file_paths = glob.glob(path_match_string)
    if file_paths is None:
        raise UserWarning("There are no matching experiment data files. No consolidated files are generated.")

    acc_df = None
    for file_path in file_paths:
        record_df = pd.read_parquet(file_path)
        if acc_df is None:
            acc_df = record_df
        else:
            acc_df = pd.concat([acc_df, record_df])
    acc_df = acc_df.reset_index(drop=True)
    acc_df = acc_df[acc_df["end_time"] > acc_df["start_time"]]

    out_file_path = (
        "_".join([
            dir_path + "expt",
            expt_method,
            dataset.replace("_", "-"),
            response_col.replace("_", "-"),
            "consolidated.parquet"
        ])
    )

    out_df = acc_df.loc[acc_df.astype(str).drop_duplicates().index]
    out_df.to_parquet(out_file_path)

    if cleanup_files:
        for file_path in file_paths:
            if "consolidated" not in file_path:
                os.remove(file_path)

    return out_file_path
