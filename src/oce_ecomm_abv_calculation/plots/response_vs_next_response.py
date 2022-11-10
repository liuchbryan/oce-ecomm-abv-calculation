import numpy as np
import pandas as pd
import os
import re
import seaborn as sns
from typing import Any, Dict


_params_olist_basketvalue_raw = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 10,
            "binrange": None,
            "discrete": None,
            "pthresh": 0,
            "pmax": 0.825,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.7,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.4,
            "gridsize": 1000,
        },
        "clip": (0, 2000),
    },
    "xlim": {
        "zoomed_out": (0, 480),
        "zoomed_in": (0, 240)
    },
    "ylim": {
        "zoomed_out": (0, 480),
        "zoomed_in": (0, 240)
    },
}


_params_olist_basketvalue_normalized = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 0.0725,
            "binrange": None,
            "discrete": None,
            "pthresh": 0,
            "pmax": 0.825,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.7,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.35,
            "gridsize": 1000,
        },
        "clip": (0, 15),
    },
    "xlim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.8)
    },
    "ylim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.8)
    },
}


_params_olist_basketsize_raw = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": None,
            "binrange": None,
            "discrete": True,
            "pthresh": 0,
            "pmax": 0.8,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 2.5,
            "levels": np.linspace(0.01, 0.96, 11),
        },
        "marginal": {
            "bw_adjust": 2.5,
            "gridsize": 4000,
        },
        "clip": (0, 10),
    },
    "xlim": {
        "zoomed_out": (0, 7),
        "zoomed_in": (0, 7)
    },
    "ylim": {
        "zoomed_out": (0, 7),
        "zoomed_in": (0, 7)
    },
}


_params_olist_basketsize_normalized = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 0.877,
            "binrange": ((0.4385, 5.7), (0.4385, 5.7)),
            "discrete": None,
            "pthresh": 0,
            "pmax": 0.8,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 2.5,
            "levels": np.linspace(0.01, 0.96, 11),
        },
        "marginal": {
            "bw_adjust": 2.5,
            "gridsize": 4000,
        },
        "clip": (0, 10),
    },
    "xlim": {
        "zoomed_out": (0, 6.1),
        "zoomed_in": (0, 6.1)
    },
    "ylim": {
        "zoomed_out": (0, 6.1),
        "zoomed_in": (0, 6.1)
    },
}


_params_uci_basketvalue_raw = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 25,
            "binrange": None,
            "discrete": None,
            "pthresh": 0.0001,
            "pmax": 0.88,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.4,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.25,
            "gridsize": 5000,
        },
        "clip": (0, 8000),
    },
    "xlim": {
        "zoomed_out": (0, 1650),
        "zoomed_in": (0, 750)
    },
    "ylim": {
        "zoomed_out": (0, 1650),
        "zoomed_in": (0, 750)
    },
}


_params_uci_basketvalue_normalized = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 0.05,
            "binrange": None,
            "discrete": None,
            "pthresh": 0.0001,
            "pmax": 0.88,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.4,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.25,
            "gridsize": 5000,
        },
        "clip": (0, 17),
    },
    "xlim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.6)
    },
    "ylim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.6)
    },
}


_params_uci_basketsize_raw = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 20,
            "binrange": None,
            "discrete": None,
            "pthresh": 0.0001,
            "pmax": 0.88,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.35,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.3,
            "gridsize": 2000,
        },
        "clip": (0, 6000),
    },
    "xlim": {
        "zoomed_out": (0, 1020),
        "zoomed_in": (0, 400)
    },
    "ylim": {
        "zoomed_out": (0, 1020),
        "zoomed_in": (0, 400)
    },
}


_params_uci_basketsize_normalized = {
    "hist": {
        "sample_frac": 1,
        "joint": {
            "binwidth": 0.07,
            "binrange": None,
            "discrete": None,
            "pthresh": 0.0001,
            "pmax": 0.88,
        }
    },
    "kde": {
        "sample_frac": 1,
        "joint": {
            "bw_adjust": 0.35,
            "levels": np.linspace(0.05, 0.95, 10),
        },
        "marginal": {
            "bw_adjust": 0.3,
            "gridsize": 2000,
        },
        "clip": (0, 20),
    },
    "xlim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.4)
    },
    "ylim": {
        "zoomed_out": (0, 3.5),
        "zoomed_in": (0, 1.4)
    },
}


def get_plot_params(dataset_name: str,
                    response_col: str,
                    normalize: bool) -> Dict[str, Any]:
    """
    Retrun the appropriate set of plot parameters based on the arguments
    :param dataset_name: Name of the dataset, e.g. `olist_brazilian_ecommerce_customer_order_view`
    or `uci_online_retail_ii_customer_order_view`
    :param response_col: Name of the response column, e.g. `r_BasketSize` or `r_BasketValue`
    :param normalize: Whether the response column is already normalized by its average value
    :return:
    """
    if "olist_brazilian_ecommerce" in dataset_name:
        if response_col == "r_BasketValue":
            if normalize:
                return _params_olist_basketvalue_normalized
            else:
                return _params_olist_basketvalue_raw
        elif response_col == "r_BasketSize":
            if normalize:
                return _params_olist_basketsize_normalized
            else:
                return _params_olist_basketsize_raw
    elif "uci_online_retail_ii" in dataset_name:
        if response_col == "r_BasketValue":
            if normalize:
                return _params_uci_basketvalue_normalized
            else:
                return _params_uci_basketvalue_raw
        if response_col == "r_BasketSize":
            if normalize:
                return _params_uci_basketsize_normalized
            else:
                return _params_uci_basketsize_raw
    raise NotImplementedError


def next_col_name(col_name: str):
    """
    :param col_name:
    :return: The name of the column representing the next event
    """
    if col_name is not None:
        return "Next" + str(col_name)
    raise UserWarning("`col_name` is None.")


def output_file_path(
        dataset_name: str,
        response_col: str,
        normalize: bool,
        plot_type: str,
        dir_path: str = f"{os.path.dirname(__file__)}/../../../data",
):
    return(
        "_".join([
            "/".join([dir_path, "plot_rvnr"]),
            dataset_name.split("_")[0],
            response_col.split("_")[1],
            str(normalize),
            plot_type + ".pdf"
        ])
    )


def append_next_analysis_unit_under_same_randomization_unit(
        df: pd.DataFrame,
        normalize_response_cols: bool = False):
    assert (
        all([
            required_col in df.columns
            for required_col in ["RandomizationUnitId", "AnalysisUnitId", "EventReceivedTime"]
        ])
    ), f"`df` is missing at least one of required columns " \
        "[`RandomizationUnitId`, `AnalysisUnitId`, `EventReceivedTime`]"

    return_df = df.copy().sort_values(["RandomizationUnitId", "EventReceivedTime"])

    if normalize_response_cols:
        response_cols = [col for col in return_df.columns
                         if col not in ["RandomizationUnitId", "AnalysisUnitId", "EventReceivedTime"]]

        return_df[response_cols] = return_df[response_cols] / return_df[response_cols].mean()

    next_analysis_unit_cols = [next_col_name(col) for col in return_df.columns if col != "RandomizationUnitId"]
    return_df[next_analysis_unit_cols] = return_df.groupby('RandomizationUnitId').shift(-1)

    return return_df


def modify_axis_labels(sns_plot: sns.JointGrid,
                       response_col: str):
    return(
        sns_plot.set_axis_labels(
            xlabel=re.sub(r"\B([A-Z])", r" \1", response_col.replace("r_", "Next")),
            ylabel=re.sub(r"\B([A-Z])", r" \1", response_col.replace("r_", ""))
        )
    )


def hist_zoomed_out_plot(plot_dataset_df: pd.DataFrame,
                         plot_params: Dict[str, Any],
                         response_col: str,
                         size: float = 3.0) -> sns.JointGrid:
    output_plot = (
        sns.jointplot(
            data=plot_dataset_df.sample(frac=plot_params["hist"]["sample_frac"]),
            x=next_col_name(response_col),
            y=response_col,
            kind="hist",
            height=size,
            joint_kws=dict(binwidth=plot_params["hist"]["joint"]["binwidth"],
                           binrange=plot_params["hist"]["joint"]["binrange"],
                           discrete=plot_params["hist"]["joint"]["discrete"],
                           pthresh=plot_params["hist"]["joint"]["pthresh"],
                           pmax=plot_params["hist"]["joint"]["pmax"],),
            marginal_kws=dict(discrete=plot_params["hist"]["joint"]["discrete"],
                              fill=True),
            xlim=plot_params["xlim"]["zoomed_out"],
            ylim=plot_params["ylim"]["zoomed_out"]
        )
    )
    return modify_axis_labels(output_plot, response_col)


def hist_zoomed_in_plot(plot_dataset_df: pd.DataFrame,
                        plot_params: Dict[str, Any],
                        response_col: str,
                        size: float = 3.0) -> sns.JointGrid:
    output_plot = (
        sns.jointplot(
            data=plot_dataset_df.sample(frac=plot_params["hist"]["sample_frac"]),
            x=next_col_name(response_col),
            y=response_col,
            kind="hist",
            height=size,
            joint_kws=dict(binwidth=plot_params["hist"]["joint"]["binwidth"],
                           binrange=plot_params["hist"]["joint"]["binrange"],
                           discrete=plot_params["hist"]["joint"]["discrete"],
                           pthresh=plot_params["hist"]["joint"]["pthresh"],
                           pmax=plot_params["hist"]["joint"]["pmax"], ),
            marginal_kws=dict(discrete=plot_params["hist"]["joint"]["discrete"],
                              fill=True),
            xlim=plot_params["xlim"]["zoomed_in"],
            ylim=plot_params["ylim"]["zoomed_in"]
        )
    )
    return modify_axis_labels(output_plot, response_col)


def kde_plot(plot_dataset_df: pd.DataFrame,
             plot_params: Dict[str, Any],
             response_col: str,
             size: float = 3.0) -> sns.JointGrid:
    output_plot = (
        sns.jointplot(
            data=plot_dataset_df.sample(frac=plot_params["kde"]["sample_frac"]),
            x=next_col_name(response_col),
            y=response_col,
            kind="kde",
            height=size,
            joint_kws=dict(bw_adjust=plot_params["kde"]["joint"]["bw_adjust"],
                           levels=plot_params["kde"]["joint"]["levels"]),
            marginal_kws=dict(bw_adjust=plot_params["kde"]["marginal"]["bw_adjust"],
                              gridsize=plot_params["kde"]["marginal"]["gridsize"],
                              fill=False),
            clip=plot_params["kde"]["clip"],
            xlim=plot_params["xlim"]["zoomed_out"],
            ylim=plot_params["ylim"]["zoomed_out"]
        )
    )
    return modify_axis_labels(output_plot, response_col)
