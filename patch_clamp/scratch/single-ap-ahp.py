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


def _fwhm(d_ap):
    half1y = d_ap["ap_y"][0 : d_ap["ap_max_index"]]
    half1x = d_ap["ap_x"][0 : d_ap["ap_max_index"]]
    half2y = d_ap["ap_y"][d_ap["ap_max_index"] :]
    half2x = d_ap["ap_x"][d_ap["ap_max_index"] :]
    half_amplitude = d_ap["ap_max_voltage"] - (d_ap["ap_amplitude"] / 2)
    distances1 = [_distance(half_amplitude, i) for i in half1y]
    distances2 = [_distance(half_amplitude, i) for i in half2y]
    half_max_ind1 = np.where(distances1 == np.min(distances1))[0]
    half_max_ind2 = np.where(distances2 == np.min(distances2))[0]
    actual_x_1 = half1x[half_max_ind1]
    actual_x_2 = half2x[half_max_ind2]
    ap_x1_index = np.where(d_ap["ap_x"] == actual_x_1)[0]
    ap_x2_index = np.where(d_ap["ap_x"] == actual_x_2)[0]
    WIDTH = actual_x_2 - actual_x_1
    return ap_x1_index, ap_x2_index, WIDTH


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
        ditem["half_x1_index"] = []
        ditem["half_x2_index"] = []
        ditem["fwhm"] = []
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
    ditem["ap_min_index"] = min_ind[0]
    ditem["ap_min_voltage"] = ditem["ap_y"][min_ind]
    ditem["ap_max_index"] = max_ind[0]
    ditem["ap_max_voltage"] = ditem["ap_y"][max_ind]
    half_max_voltage = ditem["ap_max_voltage"] / 2
    ditem["half_max_voltage"] = half_max_voltage[0]
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
    )[0]
    ditem["AHP_amplitude"] = _distance(
        ditem["firing_threshold_voltage"], ditem["ap_min_voltage"]
    )
    ap_x1_index, ap_x2_index, width = _fwhm(ditem)
    ditem["half_x1_index"] = ap_x1_index
    ditem["half_x2_index"] = ap_x2_index
    ditem["fwhm"] = width
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
        [d["ap_x"][d["half_x1_index"]], d["ap_x"][d["half_x2_index"]]],
        [d["ap_y"][d["half_x1_index"]], d["ap_y"][d["half_x2_index"]]],
        label="FWHM",
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


ctrl_2 = ap_read_filter_derivative(ctrl_array[20], 1, 2, 25)
f = plot_ap_features(ctrl_2)
plt.show()

## Look at all

for item in ap_items:
    current = ap_read_filter_derivative(item, 1, 2, 25)
    f = plot_ap_features(current)
    plt.show()
    print("NEXT")
