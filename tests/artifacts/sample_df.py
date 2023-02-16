from datetime import datetime
import pandas as pd


only_event_received_time_df = (
    pd.DataFrame([
        {"EventReceivedTime": datetime(2022, 1, 1, 0, 0, 0)},
        {"EventReceivedTime": datetime(2022, 1, 1, 23, 59, 59)},
        {"EventReceivedTime": datetime(2022, 1, 2, 0, 0, 0)},
        {"EventReceivedTime": datetime(2022, 1, 2, 12, 0, 0)},
        {"EventReceivedTime": datetime(2022, 1, 2, 23, 59, 59)},
        {"EventReceivedTime": datetime(2022, 1, 3, 0, 0, 0)},
        {"EventReceivedTime": datetime(2022, 1, 4, 0, 0, 0)},
    ])
)


sample_customer_order_df = (
    pd.DataFrame([
        {
            "RandomizationUnitId": "1",
            "AnalysisUnitId": "1a",
            "EventReceivedTime": datetime(2022, 1, 1, 0, 0, 0),
            "r_response": 5,
        },
        {
            "RandomizationUnitId": "1",
            "AnalysisUnitId": "1b",
            "EventReceivedTime": datetime(2022, 1, 1, 23, 59, 59),
            "r_response": 3,
        },
        {
            "RandomizationUnitId": "1",
            "AnalysisUnitId": "1c",
            "EventReceivedTime": datetime(2022, 1, 2, 0, 0, 0),
            "r_response": 8,
        },
        {
            "RandomizationUnitId": "1",
            "AnalysisUnitId": "1d",
            "EventReceivedTime": datetime(2022, 1, 2, 12, 0, 0),
            "r_response": 2,
        },
        {
            "RandomizationUnitId": "2",
            "AnalysisUnitId": "2a",
            "EventReceivedTime": datetime(2022, 1, 2, 23, 59, 59),
            "r_response": 9,
        },
        {
            "RandomizationUnitId": "2",
            "AnalysisUnitId": "2b",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 0, 0),
            "r_response": 1,
        },
        {
            "RandomizationUnitId": "3",
            "AnalysisUnitId": "3a",
            "EventReceivedTime": datetime(2022, 1, 4, 0, 0, 0),
            "r_response": 6,
        },
    ])
)


# This DF has more rows to reduce the chance of all rows being zero-weighted in a two-way bootstrap
sample_customer_order_item_df = (
    pd.DataFrame([
        {
            "RandomizationUnitId": "1",
            "SecondaryUnitId": "a",
            "AnalysisUnitId": "1a",
            "EventReceivedTime": datetime(2022, 1, 1, 0, 0, 0),
            "r_response": 5,
        },
        {
            "RandomizationUnitId": "1",
            "SecondaryUnitId": "b",
            "AnalysisUnitId": "1b",
            "EventReceivedTime": datetime(2022, 1, 1, 23, 59, 59),
            "r_response": 3,
        },
        {
            "RandomizationUnitId": "1",
            "SecondaryUnitId": "c",
            "AnalysisUnitId": "1c",
            "EventReceivedTime": datetime(2022, 1, 2, 0, 0, 0),
            "r_response": 8,
        },
        {
            "RandomizationUnitId": "1",
            "SecondaryUnitId": "d",
            "AnalysisUnitId": "1d",
            "EventReceivedTime": datetime(2022, 1, 2, 12, 0, 0),
            "r_response": 2,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "a",
            "AnalysisUnitId": "2a",
            "EventReceivedTime": datetime(2022, 1, 2, 23, 59, 59),
            "r_response": 9,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "b",
            "AnalysisUnitId": "2b",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 0, 0),
            "r_response": 1,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "c",
            "AnalysisUnitId": "2c",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 1, 0),
            "r_response": 6,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "d",
            "AnalysisUnitId": "2d",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 2, 0),
            "r_response": 13,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "e",
            "AnalysisUnitId": "2e",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 3, 0),
            "r_response": 222,
        },
        {
            "RandomizationUnitId": "2",
            "SecondaryUnitId": "f",
            "AnalysisUnitId": "2f",
            "EventReceivedTime": datetime(2022, 1, 3, 0, 4, 0),
            "r_response": 49,
        },
        {
            "RandomizationUnitId": "3",
            "SecondaryUnitId": "a",
            "AnalysisUnitId": "3a",
            "EventReceivedTime": datetime(2022, 1, 4, 0, 0, 0),
            "r_response": 6,
        },
        {
            "RandomizationUnitId": "3",
            "SecondaryUnitId": "b",
            "AnalysisUnitId": "3b",
            "EventReceivedTime": datetime(2022, 1, 4, 1, 0, 0),
            "r_response": 999,
        },
        {
            "RandomizationUnitId": "3",
            "SecondaryUnitId": "c",
            "AnalysisUnitId": "3c",
            "EventReceivedTime": datetime(2022, 1, 4, 2, 0, 0),
            "r_response": 1234,
        },
    ])
)
