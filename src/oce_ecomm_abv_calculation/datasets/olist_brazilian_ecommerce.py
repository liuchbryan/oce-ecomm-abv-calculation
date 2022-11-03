import os
import pandas as pd
import random
import wget

from .ecommerce_dataset import ECommerceDataset


def _download_raw_dataset_from_internet(out_path: str, file_name: str = "olist_orders_dataset.csv") -> None:
    """
    :param out_path: Destination (file path) of the dataset to be downloaded
    :param file_name: File name of the dataset, should be in the format of "olist_<dataset name>_dataset.csv"
    :return:
    """
    internet_mirror_dir_urls = [
        "https://raw.githubusercontent.com/Mortiniera/brazilian-e-commerce/master/Data/E-Commerce/",
        "https://raw.githubusercontent.com/nabeel-io/olist_database_analysis/main/olist_data/",
        "https://raw.githubusercontent.com/NoahPlage/Olist-Business-Analysis/main/data/",
        "https://raw.githubusercontent.com/VictorGuedes/Brazilian-E-Commerce-Public-Dataset-examples/master/dataset/",
        "https://raw.githubusercontent.com/dujiaying/olist/master/data/",
    ]

    for dir_url in random.sample(internet_mirror_dir_urls, k=len(internet_mirror_dir_urls)):
        try:
            dataset_url = os.path.join(dir_url, file_name)
            print(f"Downloading from {dataset_url} ...")
            actual_out_path = wget.download(dataset_url, out=out_path)
            if actual_out_path == out_path:
                return
        except:
            # If anything goes wrong, try next mirror
            continue

    raise RuntimeError("Unable to download dataset from internet. This may be due to a lost of internet connection, "
                       "the requested file not existing, or all mirrors not being available.")


class OlistBrazilianEcommerceDataset(ECommerceDataset):
    def __init__(
        self,
        path=f"{os.path.dirname(__file__)}/../../../data"
    ):
        """
        :param path: Path to the directory where the datafile is stored / should be downloaded to
        """
        # `path` can be directory or file, distinguish the use cases (here we want the directory path)
        if os.path.isdir(path):
            dir_path = path
        else:
            dir_path = os.path.dirname(path)

        # Specify file names and file paths
        customers_file_name = "olist_customers_dataset.csv"
        customers_file_path = os.path.join(dir_path, customers_file_name)
        orders_file_name = "olist_orders_dataset.csv"
        orders_file_path = os.path.join(dir_path, orders_file_name)
        order_items_file_name = "olist_order_items_dataset.csv"
        order_items_file_path = os.path.join(dir_path, order_items_file_name)

        # Download dataset from the internet if any of the required datasets are missing
        # from the specified directory
        if not os.path.exists(customers_file_path):
            _download_raw_dataset_from_internet(customers_file_path, customers_file_name)
        if not os.path.exists(orders_file_path):
            _download_raw_dataset_from_internet(orders_file_path, orders_file_name)
        if not os.path.exists(order_items_file_path):
            _download_raw_dataset_from_internet(order_items_file_path, order_items_file_name)

        customers_df = pd.read_csv(customers_file_path)
        orders_df = pd.read_csv(orders_file_path, parse_dates=["order_purchase_timestamp"])
        order_items_df = pd.read_csv(order_items_file_path)

        self.df = (
            orders_df
            .merge(customers_df,
                   how="left",
                   on="customer_id")
            .merge(order_items_df,
                   how="left",
                   on="order_id")
        )

        self.cleaned_df = None
        self.customer_order_data_df = None
        self.customer_order_item_data_df = None

    def clean_data_view(self) -> pd.DataFrame:
        # Lazy cleaning - Remove bad rows and select the relevant columns
        if self.cleaned_df is None:
            self.cleaned_df = (
                self.df[
                    ~self.df["order_status"].isin(["canceled", "created", "unavailable"]) &  # Removes 1321 (1.16%) rows
                    self.df["customer_unique_id"].notnull() &
                    self.df["product_id"].notnull()                                          # Removes 3 (<0.01%) rows
                ]
                [[
                    "order_id",
                    "order_purchase_timestamp",
                    "customer_unique_id",
                    "order_item_id",
                    "product_id",
                    "price",
                ]]
            )

        return self.cleaned_df

    def standardized_customer_order_data_view(self) -> pd.DataFrame:
        # Cached view
        if self.customer_order_data_df is None:
            cleaned_df = self.clean_data_view()

            self.customer_order_data_df = (
                cleaned_df
                .groupby(["customer_unique_id", "order_id", "order_purchase_timestamp"])
                .agg(
                    r_BasketValue=pd.NamedAgg(column="price", aggfunc="sum"),
                    r_BasketSize=pd.NamedAgg(column="product_id", aggfunc="count")
                )
                .reset_index()
                .rename(columns={
                    "customer_unique_id": "RandomizationUnitId",
                    "order_id": "AnalysisUnitId",
                    "order_purchase_timestamp": "EventReceivedTime"
                })
            )

        return self.customer_order_data_df

    def standardized_customer_order_item_data_view(self) -> pd.DataFrame:
        # Cached view
        if self.customer_order_item_data_df is None:
            cleaned_df = self.clean_data_view()
            self.customer_order_item_data_df = cleaned_df

            self.customer_order_item_data_df["AnalysisUnitId"] = (
                self.customer_order_item_data_df.apply(
                    lambda row: row['order_id'] + "_" + str(int(row['order_item_id'])),
                    axis="columns"
                )
            )

            self.customer_order_item_data_df = (
                self.customer_order_item_data_df
                .rename(columns={
                    "customer_unique_id": "RandomizationUnitId",
                    "product_id": "SecondaryUnitId",
                    "order_purchase_timestamp": "EventReceivedTime",
                    "price": "r_SellingPrice"
                })
                [["RandomizationUnitId", "SecondaryUnitId", "AnalysisUnitId",
                  "EventReceivedTime", "order_id", "r_SellingPrice"]]
            )

        return self.customer_order_item_data_df

    def summary(self):
        # DataFrame will be at order-item level
        cleaned_df = self.clean_data_view()

        return_df = (
            cleaned_df
            .groupby(lambda x: 0)  # Groupby everything
            .agg(
                num_customers=pd.NamedAgg(column="customer_unique_id", aggfunc="nunique"),
                num_orders=pd.NamedAgg(column="order_id", aggfunc="nunique"),
                num_products=pd.NamedAgg(column="product_id", aggfunc="nunique"),
                num_units=pd.NamedAgg(column="product_id", aggfunc="count"),
                total_sales=pd.NamedAgg(column="price", aggfunc="sum"),
                start_date=pd.NamedAgg(column="order_purchase_timestamp", aggfunc="min"),
                end_date=pd.NamedAgg(column="order_purchase_timestamp", aggfunc="max"),
            )
        )

        return_df["duration_days"] = return_df["end_date"] - return_df["start_date"]

        return return_df
