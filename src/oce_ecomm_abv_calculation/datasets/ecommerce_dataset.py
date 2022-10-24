from abc import ABC, abstractmethod
import pandas as pd


class ECommerceDataset(ABC):

    @abstractmethod
    def clean_dataset(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def standardized_customer_order_data(self) -> pd.DataFrame:
        """
        Returns a standardized dataframe, each row describing an order,
        with at least the following columns:
        RandomizationUnitId: The customer identifier
        AnalysisUnitId: The order identifier
        r_BasketValue: The value of the order/basket
        r_BasketSize: The size (number of items) of the order/basket
        """
        pass

    @abstractmethod
    def standardized_customer_order_item_data(self) -> pd.DataFrame:
        """
        Returns a standardized dataframe, each row describing an item 
        within an order, with at least the following columns:
        RandomizationUnitId: The customer identifier
        SecondaryUnitId: The product / stock keeping unit (SKU) identifier
        AnalysisUnitId: The identifier for the item within an order 
                        (often in format of `<order>_<item>`)
        r_SellingPrice: The price of the item sold
        """
        pass
