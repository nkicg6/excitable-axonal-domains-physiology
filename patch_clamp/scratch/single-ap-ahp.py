# play
# https://github.com/pspratt/pyibt


import matplotlib.pyplot as plt
import pyabf
import scipy.signal as s
import numpy as np

from patch_clamp import database as db
from patch_clamp import ap_analysis as ap


db_path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
ap_items = [ap.peaks_to_int_list(i) for i in db.sql_data_as_dict(db_path, ap.QUERY)]


def _distance(y1, y2):
    inner = (y2 - y1) ** 2
    d = np.sqrt(inner)
    return d


def ap_read_filter_derivative(
    d, ms_window_pre, ms_window_post, threshold, golay_window_pts=19
):
    ditem = d.copy()
    try:
        # bail out if no peaks, and return empty lists for all of the
        # new keys.
        first_index = ditem["peak_index"][0]
    except IndexError:
        ditem["ap_x"] = []
        ditem["ap_y"] = []
        ditem["dydx"] = []
        ditem["max_dydx"] = []
        ditem["max_dydx_index"] = []
        ditem["ap_max_index"] = []
        ditem["ap_max_voltage"] = []
        ditem["firing_threshold_voltage"] = []
        ditem["firing_threshold_index"] = []
        ditem["ap_amplitude"] = []
        ditem["ap_min_index"] = []
        ditem["ap_min_voltage"] = []
        ditem["AHP_amplitude"] = []
        return ditem
    abf = pyabf.ABF(ditem["fpath"])
    abf.setSweep(ditem["sweep"])
    y_filtered = s.savgol_filter(abf.sweepY, golay_window_pts, 3)
    ms_window_pre = int(abf.dataPointsPerMs * ms_window_pre)
    ms_window_post = int(abf.dataPointsPerMs * ms_window_post)
    start = first_index - ms_window_pre
    stop = first_index + ms_window_post
    ditem["ap_y"] = y_filtered[start:stop]
    ditem["ap_x"] = abf.sweepX[start:stop]
    max_ind = np.where(ditem["ap_y"] == np.max(ditem["ap_y"]))[0]
    min_ind = np.where(ditem["ap_y"] == np.min(ditem["ap_y"]))[0]
    ditem["ap_min_index"] = min_ind
    ditem["ap_min_voltage"] = ditem["ap_y"][min_ind]
    ditem["ap_max_index"] = max_ind
    ditem["ap_max_voltage"] = ditem["ap_y"][max_ind]
    ditem["dydx"] = (
        np.diff(ditem["ap_y"]) / np.diff(ditem["ap_x"])
    ) / 1000  # to V from mV
    max_dydx_ind = np.where(ditem["dydx"] == np.max(ditem["dydx"]))[0]
    max_dydx = ditem["dydx"][max_dydx_ind]
    ditem["max_dydx"] = max_dydx
    ditem["max_dydx_index"] = max_dydx_ind
    f_thresh_index = np.where(ditem["dydx"] > threshold)[0][0]
    ditem["firing_threshold_voltage"] = ditem["ap_y"][f_thresh_index]
    ditem["firing_threshold_index"] = f_thresh_index
    ditem["ap_amplitude"] = _distance(
        ditem["ap_max_voltage"], ditem["firing_threshold_voltage"]
    )
    ditem["AHP_amplitude"] = _distance(
        ditem["firing_threshold_voltage"], ditem["ap_min_voltage"]
    )
    return ditem


# plot
occl_array = [i for i in ap_items if i["treatment"].lower().strip() == "occl"]
ctrl_array = [i for i in ap_items if i["treatment"].lower().strip() == "sham"]


def plot_ap_features(d):
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    if isinstance(d["ap_y"], list):
        print("No data")
        print(f"{d['fname']}-{d['treatment']}-{d['cell_side']}")
        return fig
    ax1.plot(d["ap_x"], d["ap_y"])
    ax1.plot(
        d["ap_x"][d["firing_threshold_index"]],
        d["ap_y"][d["firing_threshold_index"]],
        "r*",
        label="Threshold",
    )
    ax1.plot(
        d["ap_x"][d["ap_max_index"]],
        d["ap_y"][d["ap_max_index"]],
        "y*",
        label="Max amplitude",
    )

    ax1.plot(
        [
            d["ap_x"][d["firing_threshold_index"]],
            d["ap_x"][d["firing_threshold_index"]],
        ],
        [d["firing_threshold_voltage"], d["ap_max_voltage"]],
        color="red",
        label="Max amplitude",
    )
    ax1.plot(
        [d["ap_x"][d["ap_min_index"]], d["ap_x"][d["ap_min_index"]]],
        [d["ap_min_voltage"], d["firing_threshold_voltage"]],
        color="green",
        label="AHP amplitude",
    )

    ax2.plot(d["ap_y"][:-1], d["dydx"])
    ax2.plot(
        d["ap_y"][d["firing_threshold_index"]],
        d["dydx"][d["firing_threshold_index"]],
        "r*",
        label="Threshold",
    )
    ax2.plot(
        d["ap_y"][d["ap_max_index"]],
        d["dydx"][d["ap_max_index"]],
        "y*",
        label="Max amplitude",
    )
    ax2.plot(
        d["ap_y"][d["max_dydx_index"]],
        d["dydx"][d["max_dydx_index"]],
        "b*",
        label="max dydx",
    )
    ax2.legend()
    ax1.legend()

    fig.suptitle(f"{d['fname']}-{d['treatment']}-{d['cell_side']}")
    return fig


f = plot_ap_features(ap_read_filter_derivative(ctrl_array[20], 1, 2, 25))
plt.show()

##

occl_example = ap_read_filter_derivative(occl_array[22], 1, 2, 25)
ctrl_example = ap_read_filter_derivative(ctrl_array[23], 1, 2, 25)

single_axis = np.arange(len(occl_example["ap_x"]))
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
ax1.plot(single_axis, occl_example["ap_y"], color="red")
ax1.plot(single_axis, ctrl_example["ap_y"], color="blue")
ax1.plot(
    single_axis[occl_example["ap_max_ind"]],
    occl_example["ap_y"][occl_example["ap_max_ind"]],
    "y*",
)
ax1.plot(
    single_axis[ctrl_example["ap_max_ind"]],
    ctrl_example["ap_y"][ctrl_example["ap_max_ind"]],
    "g*",
)
ax2.plot(
    ctrl_example["ap_y"][:-1],
    ctrl_example["dydx"],
    color="blue",
    label=f"Control-{ctrl_example['cell_side']}",
)
ax2.plot(
    occl_example["ap_y"][:-1],
    occl_example["dydx"],
    color="red",
    label=f"Occluded-{occl_example['cell_side']}",
)
ax2.legend()
ax2.yaxis.tick_right()
plt.show()
