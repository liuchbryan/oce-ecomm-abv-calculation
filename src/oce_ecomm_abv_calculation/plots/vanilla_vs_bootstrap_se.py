from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import t
from typing import Any, Dict, List, Optional, Union


def get_plot_statistics_from_experiment_results_file(
    vanilla_experiment_results_df: pd.DataFrame,
    bootstrap_experiment_results_df: pd.DataFrame,
    normalize_se: bool = True
):
    """

    :param vanilla_experiment_results_df:
    :param bootstrap_experiment_results_df:
    :param normalize_se: Whether the SE columns should be normalized by the first SE evaluation. Default `True`.
    This does not affect the bootstrap SE / vanilla SE ratio calculations.
    :return:
    """
    groupby_cols = ["dataset_name", "response_col", "start_time", "end_time", "count"]

    combined_experiment_results_df = (
        vanilla_experiment_results_df.merge(
            bootstrap_experiment_results_df,
            on=groupby_cols,
            how="inner"
        )
    )

    plot_statistics_df = (
        combined_experiment_results_df
        .groupby(groupby_cols)
        .agg(sample_standard_error=pd.NamedAgg(column="sample_standard_error", aggfunc="first"),
             bootstrap_standard_error_mean=pd.NamedAgg(column="bootstrap_standard_error", aggfunc="mean"),
             bootstrap_standard_error_stddev=pd.NamedAgg(column="bootstrap_standard_error", aggfunc="std"),
             bootstrap_standard_error_count=pd.NamedAgg(column="bootstrap_standard_error", aggfunc="count"))
        .reset_index()
        .sort_values('end_time')
    )

    plot_statistics_df['days_elapsed'] = (plot_statistics_df['end_time'] - plot_statistics_df['start_time']).dt.days
    plot_statistics_df['prop_time_elapsed'] = (
            plot_statistics_df['days_elapsed'] / plot_statistics_df['days_elapsed'].max()
    )

    # Normalize raw standard error by the standard error during first evaluation
    if normalize_se:
        first_day_sample_standard_error = plot_statistics_df['sample_standard_error'][0]
        plot_statistics_df['sample_standard_error'] = (
            plot_statistics_df['sample_standard_error'] / first_day_sample_standard_error
        )
        plot_statistics_df['bootstrap_standard_error_mean'] = (
            plot_statistics_df['bootstrap_standard_error_mean'] / first_day_sample_standard_error
        )
        plot_statistics_df['bootstrap_standard_error_stddev'] = (
            plot_statistics_df['bootstrap_standard_error_stddev'] / first_day_sample_standard_error
        )

    plot_statistics_df['bootstrap_standard_error_mean_ratio'] = (
        plot_statistics_df['bootstrap_standard_error_mean'] /
        plot_statistics_df['sample_standard_error']
    )
    plot_statistics_df['bootstrap_standard_error_stddev_ratio'] = (
        plot_statistics_df['bootstrap_standard_error_stddev'] /
        plot_statistics_df['sample_standard_error']
    )

    return plot_statistics_df


def get_plot_parameters(plot_statistics_df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
    """
    Get the plot parameters for the bootstrap se / vanilla se ratio plots, use `kwargs` to override
    :param plot_statistics_df: ONE plot statistics dataframe (representing reuslts from one dataset)
    :return: Dict containing the plot parameters to be fed directly into plt.plot() (and equivalent functions)
    """
    dataset_name = plot_statistics_df["dataset_name"].iloc[0]

    plot_color_mapping = {
        "asos_customer_order_view": "tab:orange",
        "asos_customer_order_item_view": "tab:orange",
        "uci_online_retail_ii_customer_order_view": "tab:green",
        "uci_online_retail_ii_customer_order_item_view": "tab:green",
        "olist_brazilian_ecommerce_customer_order_view": "tab:blue",
        "olist_brazilian_ecommerce_customer_order_item_view": "tab:blue",
    }

    plot_marker_mapping = {
        "asos_customer_order_view": None,
        "asos_customer_order_item_view": None,
        "uci_online_retail_ii_customer_order_view": "^",
        "uci_online_retail_ii_customer_order_item_view": "^",
        "olist_brazilian_ecommerce_customer_order_view": "o",
        "olist_brazilian_ecommerce_customer_order_item_view": "o",
    }

    plot_markersize_mapping = {
        "uci_online_retail_ii_customer_order_view": 4,
        "uci_online_retail_ii_customer_order_item_view": 4,
        "olist_brazilian_ecommerce_customer_order_view": 3,
        "olist_brazilian_ecommerce_customer_order_item_view": 3,
    }

    plot_label_mapping = {
        "asos_customer_order_view": "ASOS",
        "asos_customer_order_item_view": "ASOS",
        "uci_online_retail_ii_customer_order_view": "UCI",
        "uci_online_retail_ii_customer_order_item_view": "UCI",
        "olist_brazilian_ecommerce_customer_order_view": "Olist",
        "olist_brazilian_ecommerce_customer_order_item_view": "Olist",
    }

    return {
        "color": (plot_color_mapping[dataset_name]
                  if dataset_name in plot_color_mapping else None),
        "marker": (plot_marker_mapping[dataset_name]
                   if dataset_name in plot_marker_mapping else None),
        "markersize": (plot_markersize_mapping[dataset_name]
                       if dataset_name in plot_markersize_mapping else None),
        "label": kwargs["label"] if "label" in kwargs else(
            plot_label_mapping[dataset_name] if dataset_name in plot_label_mapping else None),
    }


def _get_days_elapsed_scale_major_ticks(plot_statistics_dfs: List[pd.DataFrame]) -> Optional[List[int]]:
    """
    Return the list of major tick marks used in Vanilla SE vs Bootstrap SE plots.
    Only applicable if the x-axis scale reference is set to "days elapsed", where log-scale is used by default.
    The list is dependent on the max number of days featured in dataset(s) as described by `plot_statistics_dfs`.
    It goes by [1, 10, 100, ...], where the last value on the list is the last order of magnitude that is smaller
    than 1.05x the max number of days elapsed in the dataset(s).
    e.g., Max days = 50 => [1, 10]; Max days = 800 => [1, 10, 100]; Max days = 999 => [1, 10, 100, 1000]
    :param plot_statistics_dfs: List of plot statistics dataframes
    :return:
    """
    if plot_statistics_dfs is None:
        return None

    max_days = max([plot_statistics_df["days_elapsed"].max()
                    for plot_statistics_df in plot_statistics_dfs])
    max_major_tick_order_mag = int(np.floor(np.log10(max_days * 1.05)))
    return [10 ** order_mag for order_mag in range(0, max_major_tick_order_mag + 1)]


def _get_days_elapsed_scale_minor_ticks(plot_statistics_dfs: List[pd.DataFrame]) -> Optional[List[int]]:
    """
    Return the list of minor tick marks used in Vanilla SE vs Bootstrap SE plots.
    Only applicable if the x-axis scale reference is set to "days elapsed", where log-scale is used by default.
    The list is dependent on the max number of days featured in dataset(s) as described by `plot_statistics_dfs`.
    It goes by [2, 3, 4, 5, 6, 7, 8, 9, 20, 30, 40, 50, 60, 70, 80, 90, 200, 300, ...], where the last value on the
    list is the last natural number multiple of the respective order of magnitude that is smaller than 1.05x the
    max number of days elapsed in the dataset(s).
    e.g., Max days = 50 => [2, ..., 9, 20, 30, 40, 50]; Max days = 365 => [2, ..., 9, 20, ..., 90, 200, 300];
    Max days = 880 => [2, ..., 9, 20, ..., 90, 200, ..., 800, 900].
    :param plot_statistics_dfs: List of plot statistics dataframes
    :return:
    """
    if plot_statistics_dfs is None:
        return None

    max_days = max([plot_statistics_df["days_elapsed"].max()
                    for plot_statistics_df in plot_statistics_dfs])
    max_major_tick_order_mag = int(np.floor(np.log10(max_days * 1.05)))
    minor_ticks = (
        [multiplier * 10 ** order_mag
         for multiplier in [2, 3, 4, 5, 6, 7, 8, 9]
         for order_mag in range(0, max_major_tick_order_mag + 1)
         if multiplier * 10 ** order_mag < max_days * 1.05]
    )
    minor_ticks.sort()
    return minor_ticks


def _set_x_axis_according_to_scale_reference(
    ax: plt.axis,
    xaxis_scale_reference: str,
    plot_statistics_dfs: List[pd.DataFrame]
):
    """
    :param ax: Matplotlib axis generated by e.g., plt.subplot()
    :param xaxis_scale_reference: Which column within `plot_statistics_dfs` should we use as the reference for the
    x-axis. Options: ("end_time", "days_elapsed", "prop_time_elapsed")
    :param plot_statistics_dfs: List of plot statistics dataframes
    :return:
    """
    if xaxis_scale_reference == "days_elapsed":
        ax.set_xscale("log")
        ax.set_xticks(_get_days_elapsed_scale_major_ticks(plot_statistics_dfs),
                      _get_days_elapsed_scale_major_ticks(plot_statistics_dfs),
                      minor=False)
        ax.set_xticks(_get_days_elapsed_scale_minor_ticks(plot_statistics_dfs),
                      minor=True)
        ax.tick_params(which='major', length=5)
        ax.tick_params(which='minor', length=3)
    elif xaxis_scale_reference == "prop_time_elapsed":
        ax.set_xlim(-0.01, 1.02)
        ax.set_xticks([0, 0.5, 1], [0, 0.5, 1])
    elif xaxis_scale_reference == "end_time":
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")

    return ax


def plot_one_bootstrap_versus_vanilla_se_plot(
    ax: plt.axis,
    xaxis_scale_reference: str,
    plot_statistics_df: Union[List[pd.DataFrame], pd.DataFrame]
):
    """
    Plot one bootstrap se / vanilla se ratio plot on the given `ax`.
    :param ax: Matplotlib axis generated by e.g., plt.subplot()
    :param xaxis_scale_reference: Which column within `plot_statistics_dfs` should we use as the reference for the
    x-axis. Options: ("end_time", "days_elapsed", "prop_time_elapsed")
    :param plot_statistics_df: One plot statistics dataframe
    :return:
    """
    _plot_statistics_df = plot_statistics_df if isinstance(plot_statistics_df, pd.DataFrame) else plot_statistics_df[0]

    ax.errorbar(
        x=_plot_statistics_df[xaxis_scale_reference],
        y=_plot_statistics_df['sample_standard_error'],
        fmt='--',
        c='k',
        label="Vanilla SE"
    )

    ax.errorbar(
        x=_plot_statistics_df[xaxis_scale_reference],
        y=_plot_statistics_df['bootstrap_standard_error_mean'],
        yerr=(_plot_statistics_df['bootstrap_standard_error_stddev'] *
              t.ppf(0.975, df=_plot_statistics_df['bootstrap_standard_error_count'])),
        **get_plot_parameters(_plot_statistics_df, label="Bootstrap SE"),
    )

    ax = _set_x_axis_according_to_scale_reference(ax, xaxis_scale_reference, [_plot_statistics_df])
    return ax


def plot_one_bootstrap_vanilla_se_ratio_plot(
    ax: plt.axis,
    xaxis_scale_reference: str,
    plot_statistics_dfs: Union[pd.DataFrame, List[pd.DataFrame]]
):
    """
    Plot one bootstrap se / vanilla se ratio plot on the given `ax`.
    :param ax: Matplotlib axis generated by e.g., plt.subplot()
    :param xaxis_scale_reference: Which column within `plot_statistics_dfs` should we use as the reference for the
    x-axis. Options: ("end_time", "days_elapsed", "prop_time_elapsed")
    :param plot_statistics_dfs: List of plot statistics dataframes
    :return:
    """
    _plot_statistics_dfs = plot_statistics_dfs if isinstance(plot_statistics_dfs, list) else [plot_statistics_dfs]

    ax.axhline(y=1.0, ls='--', c='k')

    for plot_statistics_df in _plot_statistics_dfs:
        ax.errorbar(
            x=plot_statistics_df[xaxis_scale_reference],
            y=plot_statistics_df['bootstrap_standard_error_mean_ratio'],
            yerr=(plot_statistics_df['bootstrap_standard_error_stddev_ratio'] *
                  t.ppf(0.975, df=plot_statistics_df['bootstrap_standard_error_count'])),
            **get_plot_parameters(plot_statistics_df)
        )

    ax = _set_x_axis_according_to_scale_reference(ax, xaxis_scale_reference, _plot_statistics_dfs)
    return ax
