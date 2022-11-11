import os
import pandas as pd
import wget

from .ecommerce_dataset import ECommerceDataset


stock_code_exclusion_list = [
    "ADJUST",  # Manual adjustments
    "ADJUST2",
    "M",
    "m",
    "AMAZONFEE",  # Amazon fee / bank charges
    "B",
    "BANK CHARGES",
    "C2",  # Carriage / Postage
    "C3",
    "DOT",
    "POST",
    "D",  # Discounts
    "S",  # Sample
    "TEST001",  # Test products
    "TEST002",
    "CRUK",  # Commission
    "gift_0001_10",  # Gift vouchers
    "gift_0001_20",
    "gift_0001_30",
    "gift_0001_40",
    "gift_0001_50",
    "gift_0001_60",
    "gift_0001_70",
    "gift_0001_80",
    "gift_0001_90"
]


def _download_raw_dataset_from_internet(out_path) -> None:
    dataset_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx'
    wget.download(dataset_url, out=out_path)


class UCIOnlineRetailIIDataset(ECommerceDataset):
    def __init__(
        self,
        path=f"{os.path.dirname(__file__)}/../../../data"
    ):
        """
        :param path: Path to the directory where the datafile is stored / should be downloaded to
        """
        # `path` can be directory or file, distinguish the use cases
        if os.path.isdir(path):
            file_path = os.path.join(path, "online_retail_II.xlsx")
        else:
            file_path = path

        # Download dataset from the internet if no file exist at provided path
        if not os.path.exists(file_path):
            _download_raw_dataset_from_internet(out_path=file_path)

        self.df = (
            pd.concat(
                [pd.read_excel(file_path, "Year 2009-2010", index_col=None),
                 pd.read_excel(file_path, "Year 2010-2011", index_col=None)],
                ignore_index=True
            )
        )

        self.cleaned_df = None
        self.customer_order_data_df = None
        self.customer_order_item_data_df = None

    def clean_data_view(self) -> pd.DataFrame:
        # Lazy dataset cleaning
        # First four conditions remove ~30k rows (2.85% of total)
        # Last filter (exc. unknown customer orders) removes a further ~213k rows (20% of total)
        if self.cleaned_df is None:
            self.cleaned_df = (
                self.df[
                    ~(self.df["Invoice"].str.startswith('C', na=False)) &  # Exc. cancelled orders
                    (self.df["Quantity"] > 0) &  # Exc. negative quantities
                    ~(self.df["StockCode"].isin(stock_code_exclusion_list)) &  # Exc. non-stock items
                    (self.df["Price"] > 0) &  # Exc. -ve priced items
                    (self.df["Customer ID"].notnull())  # Exc. unknown customer orders
                ]
                .astype({"StockCode": "str", "Customer ID": int})
            )

            # The minimal key for this dataset is ("Invoice", "StockCode", "Description", "InvoiceDate", "Price")
            # We trim that down to ("Invoice", "StockCode", "Price"). See associated unit test for more details.
            # Removes ~33k rows (3.12% of total) but functionally should not make very little difference
            self.cleaned_df = (
                self.cleaned_df
                .groupby(["Invoice", "StockCode", "Price", "Customer ID", "Country"])
                .agg(Description=pd.NamedAgg(column="Description", aggfunc="first"),
                     Quantity=pd.NamedAgg(column="Quantity", aggfunc="sum"),
                     InvoiceDate=pd.NamedAgg(column="InvoiceDate", aggfunc="min"))
                .reset_index()
            )

            self.cleaned_df['Subtotal'] = (
                    self.cleaned_df['Quantity'] * self.cleaned_df['Price']
            )

        return self.cleaned_df

    def standardized_customer_order_data_view(self) -> pd.DataFrame:
        # Cached view
        if self.customer_order_data_df is None:
            cleaned_df = self.clean_data_view()

            self.customer_order_data_df = (
                cleaned_df
                .groupby(["Customer ID", "Invoice"])
                .agg(
                    InvoiceDate=pd.NamedAgg(column="InvoiceDate", aggfunc="first"),
                    r_BasketValue=pd.NamedAgg(column="Subtotal", aggfunc="sum"),
                    r_BasketSize=pd.NamedAgg(column="Quantity", aggfunc="sum")
                )
                .reset_index()
                .rename(columns={
                    "Customer ID": "RandomizationUnitId",
                    "Invoice": "AnalysisUnitId",
                    "InvoiceDate": "EventReceivedTime"
                })
            )

        return self.customer_order_data_df

    def standardized_customer_order_item_data_view(self) -> pd.DataFrame:
        # Cached view
        if self.customer_order_item_data_df is None:
            cleaned_df = self.clean_data_view()

            # Create index for each item/unit of the same product bought
            # and explode the dataframe so that each row contains one item at a certain price in each order
            cleaned_df['ItemIndex'] = (
                cleaned_df['Quantity'].apply(lambda quantity: list(range(1, quantity + 1)))
            )
            target_df = cleaned_df.explode(column="ItemIndex", ignore_index=True)
            target_df['AnalysisUnitId'] = (
                target_df.apply(
                    lambda row: (
                        str(row['Invoice']) + "_" +
                        row['StockCode'] + "_" +
                        str(row['Price']) + "_" +
                        str(row['ItemIndex'])
                    ),
                    axis="columns"
                )
            )

            self.customer_order_item_data_df = (
                target_df
                .rename(columns={
                    "Customer ID": "RandomizationUnitId",
                    "StockCode": "SecondaryUnitId",
                    "InvoiceDate": "EventReceivedTime",
                    "Price": "r_SellingPrice"
                })
                [["RandomizationUnitId", "AnalysisUnitId", "SecondaryUnitId",
                  "Invoice", "EventReceivedTime", "r_SellingPrice"]]
            )

        return self.customer_order_item_data_df

    def summary(self) -> pd.DataFrame:
        cleaned_df = self.clean_data_view()

        return_df = (
            cleaned_df
            .groupby(lambda x: 0)  # Groupby everything
            .agg(
                num_customers=pd.NamedAgg(column="Customer ID", aggfunc="nunique"),
                num_orders=pd.NamedAgg(column="Invoice", aggfunc="nunique"),
                num_products=pd.NamedAgg(column="StockCode", aggfunc="nunique"),
                num_units=pd.NamedAgg(column="Quantity", aggfunc="sum"),
                total_sales=pd.NamedAgg(column="Subtotal", aggfunc="sum"),
                start_date=pd.NamedAgg(column="InvoiceDate", aggfunc="min"),
                end_date = pd.NamedAgg(column="InvoiceDate", aggfunc="max"),
            )
        )

        return_df["duration_days"] = return_df["end_date"] - return_df["start_date"]

        return return_df
