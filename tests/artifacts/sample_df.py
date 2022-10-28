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
