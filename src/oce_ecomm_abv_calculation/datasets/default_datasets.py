import pandas as pd
from typing import Optional

from .uci_online_retail_ii import UCIOnlineRetailIIDataset


def get_default_dataset_by_name(dataset_name: Optional[str]) -> Optional[pd.DataFrame]:
    if dataset_name is None:
        return None
    elif "uci_online_retail_ii" in dataset_name.lower():
        if "customer_order_item" in dataset_name.lower():
            uci_online_retail_ii_customer_order_item_view()
        elif "customer_order" in dataset_name.lower():
            return uci_online_retail_ii_customer_order_view()

    return None


def uci_online_retail_ii_customer_order_view() -> pd.DataFrame:
    return UCIOnlineRetailIIDataset().standardized_customer_order_data_view()


def uci_online_retail_ii_customer_order_item_view() -> pd.DataFrame:
    return UCIOnlineRetailIIDataset().standardized_customer_order_item_data_view()
