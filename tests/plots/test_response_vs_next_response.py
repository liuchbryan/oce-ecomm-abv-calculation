import pandas as pd
import pytest

from oce_ecomm_abv_calculation.datasets.olist_brazilian_ecommerce import OlistBrazilianEcommerceDataset
from oce_ecomm_abv_calculation.plots.response_vs_next_response import \
    append_next_analysis_unit_under_same_randomization_unit, randomly_shuffle_next_analysis_unit_rows
from ..artifacts.sample_df import sample_customer_order_df, sample_customer_order_item_df


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


class TestRandomlyShuffleNextAnalysisUnitRows:
    def test_return_df_with_same_columns(self):
        input_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_df)
        output_df = randomly_shuffle_next_analysis_unit_rows(input_df)

        assert set(input_df.columns) == set(output_df.columns)

    def test_return_df_with_same_number_of_rows(self):
        input_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_item_df)
        output_df = randomly_shuffle_next_analysis_unit_rows(input_df)

        assert (input_df.shape[0] == output_df.shape[0])

    def test_original_responses_are_the_same(self):
        input_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_item_df)
        output_df = randomly_shuffle_next_analysis_unit_rows(input_df)

        assert(all(pd.Series(input_df['AnalysisUnitId'] == output_df['AnalysisUnitId'])))

    def test_next_responses_are_still_the_same_set(self):
        input_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_item_df)
        output_df = randomly_shuffle_next_analysis_unit_rows(input_df)

        assert set(input_df['NextAnalysisUnitId']) == set(output_df['NextAnalysisUnitId'])

    def test_next_responses_are_randomly_shuffled(self):
        input_df = append_next_analysis_unit_under_same_randomization_unit(sample_customer_order_item_df)
        # Some responses might still end up with the same next response after random shuffling due to chance.
        # Here we say it is fine if the proportion of rows ending up with the same next response is small.
        try:
            output_df = randomly_shuffle_next_analysis_unit_rows(input_df)
            next_analysis_unit_id_equal = pd.Series(input_df['NextAnalysisUnitId'] == output_df['NextAnalysisUnitId'])

            assert next_analysis_unit_id_equal.mean() <= (2 / 13)
        except AssertionError:
            # The test DF has 13 rows, and it is possible to have >2 rows ending up with the same next response.
            # In this case we try again.
            output_df = randomly_shuffle_next_analysis_unit_rows(input_df)
            next_analysis_unit_id_equal = pd.Series(input_df['NextAnalysisUnitId'] == output_df['NextAnalysisUnitId'])

            assert next_analysis_unit_id_equal.mean() <= (2 / 13)
