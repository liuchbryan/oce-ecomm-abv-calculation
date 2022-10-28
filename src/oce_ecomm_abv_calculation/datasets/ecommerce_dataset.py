from abc import ABC, abstractmethod
import pandas as pd


class ECommerceDataset(ABC):

    @abstractmethod
    def clean_data_view(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def standardized_customer_order_data_view(self) -> pd.DataFrame:
        """
        :return: A standardized dataframe, each row describing an order,
        with at least the following columns:
        RandomizationUnitId: The customer identifier
        AnalysisUnitId: The order identifier
        r_BasketValue: The value of the order/basket
        r_BasketSize: The size (number of items) of the order/basket
        """
        pass

    @abstractmethod
    def standardized_customer_order_item_data_view(self) -> pd.DataFrame:
        """
        :return: A standardized dataframe, each row describing an item
        within an order, with at least the following columns:
        RandomizationUnitId: The customer identifier
        SecondaryUnitId: The product / stock keeping unit (SKU) identifier
        AnalysisUnitId: The identifier for the item within an order 
                        (often in format of `<order>_<item>`)
        r_SellingPrice: The price of the item sold
        """
        pass

    @abstractmethod
    def summary(self) -> pd.DataFrame:
        """
        :return: Summary statistics on the number of distinct customers, orders/baskets,
        products/SKUs, items/units, and total amount of sales in the dataset.
        Ideally this summary statistics referred to the dataframe obtained via
        `clean_data_view()`.
        """
        pass
