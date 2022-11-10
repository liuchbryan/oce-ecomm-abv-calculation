import pytest

from oce_ecomm_abv_calculation.datasets.olist_brazilian_ecommerce import OlistBrazilianEcommerceDataset
from oce_ecomm_abv_calculation.plots.response_vs_next_response import \
    append_next_analysis_unit_under_same_randomization_unit
from ..artifacts.sample_df import sample_customer_order_df


class TestAppendNextAnalysisUnitUnderSameRandomizationUnit:
    def test_return_df_with_necessary_columns(self):
        assert all([col in sample_customer_order_df.columns
                    for col in ["RandomizationUnitId", "AnalysisUnitId", "EventReceivedTime", "r_response"]])

        actual_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_df)

        assert all([col in actual_df.columns
                    for col in ["RandomizationUnitId",
                                "AnalysisUnitId",
                                "EventReceivedTime",
                                "r_response",
                                "NextAnalysisUnitId",
                                "NextEventReceivedTime",
                                "Nextr_response"]])

    def test_return_df_with_all_rows_of_df(self):
        actual_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_df)
        assert actual_df.shape[0] == sample_customer_order_df.shape[0]
        assert set(actual_df['RandomizationUnitId']) == set(sample_customer_order_df['RandomizationUnitId'])

    def test_normalize_response_cols_normalizes_response_cols(self):
        actual_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_df,
                                                                            normalize_response_cols=True)

        assert actual_df["r_response"].mean() == 1.0

    def test_normalize_response_cols_normalizes_next_response_cols_by_original_response_mean(self):
        actual_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_df,
                                                                            normalize_response_cols=True)
        # Normalize using only the non-null values in `Nextr_response` is wrong
        assert actual_df["Nextr_response"].mean() != 1.0
        # Average `r_response` in this dataset is 34/7
        assert actual_df["Nextr_response"].mean() == pytest.approx((3.0 + 8.0 + 2.0 + 1.0) / (34.0 / 7) / 4, abs=1e-12)

    def test_normalize_response_cols_handles_multiple_response_cols(self):
        actual_df = append_next_analysis_unit_under_same_randomization_unit(
            OlistBrazilianEcommerceDataset().standardized_customer_order_data_view(),
            normalize_response_cols=True)

        assert actual_df["r_BasketValue"].mean() == pytest.approx(1.0, abs=1e-12)
        assert actual_df["r_BasketSize"].mean() == pytest.approx(1.0, abs=1e-12)
