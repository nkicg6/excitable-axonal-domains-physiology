# analysis for patch clamp current steps analysis
import os
import pyabf
import numpy as np
import scipy.signal as s


cc01test = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-04/20104002.abf"


def read_abf_IO(path, sweep, channel):
    """reads an abf file at a specific sweep.
    returns X,Y data for that sweep and"""
    short = os.path.split(path)[-1].replace(".abf", "")
    try:
        abf = pyabf.ABF(path)
        abf.setSweep(sweepNumber=sweep, channel=channel)
        data = {
            "path": path,
            "sweep": sweep,
            "sweep_list": abf.sweepList,
            "channel": channel,
            "x": abf.sweepX,
            "y": abf.sweepY,
            "short_name": short,
            "protocol": abf.protocol,
            "error": [],
        }
        return data
    except Exception as e:
        print(e)
        return {
            "path": path,
            "sweep": sweep,
            "sweep_list": [],
            "channel": channel,
            "x": np.asarray([]),
            "y": np.asarray([]),
            "short_name": short,
            "protocol": "unknown",
            "error": [f"io error: {e}"],
        }


def abf_golay(abfd, window=11, polyorder=3):
    """applies scipy implementation of the Savitzky-Golay filter to data `y`. returns
    original dict with a new key `filtered` containing the filtered data, or an empty
    array. If array is empty, adds a `filter error` to the error list"""
    abf = abfd.copy()
    try:
        filtered = s.savgol_filter(abf["y"], polyorder=polyorder, window_length=window)
    except ValueError as e:
        filtered = np.asarray([])
        abf["error"].append(f"filter error: {e}")
    abf["filtered"] = filtered
    abf["savgol_details"] = {"polyorder": polyorder, "window": window}
    return abf


def count_spikes(abfd, threshold=0.25, use_filtered=True):
    """takes an abf data structure and counts the spikes based on the `threshold` given.
    Threshold is the % above the mean value to set the spike threshold. This assumes the
    mean value will be negative."""
    abf = abfd.copy()
    if use_filtered:
        data = abf["filtered"].copy()
        filt_opt = True  # track branch taken
    if not use_filtered:
        data = abf["y"].copy()
        filt_opt = False  # track branch taken
    if data.size == 0:
        abf["peaks"] = np.asarray([])
        abf["peak_props"] = {"no_data": "no_data"}
        abf["peak_props"]["threshold"] = None
        abf["peak_props"]["use_filtered?"] = filt_opt
        return abf
    threshold = abs(data.mean() * threshold) + data.mean()
    peaks, props = s.find_peaks(data, height=threshold, distance=15, prominence=5)
    abf["peaks"] = peaks
    abf["peak_props"] = props
    abf["peak_props"]["threshold"] = threshold
    abf["peak_props"]["use_filtered?"] = filt_opt
    return abf


def filter_stim_indicies_cc01(abfd):
    abf = abfd.copy()
    assert abf["protocol"] == "cc_01-steps"
    start_x_ind = np.where(abf["x"][abf["peaks"]] > abf["x"][10625])[0][0]
    stop_x_ind = np.where(abf["x"][abf["peaks"]] < abf["x"][30627])[0][-1]
    abf["during_stim_peaks"] = abf["peaks"][start_x_ind:stop_x_ind]
    print(f"len peaks {len(abf['peaks'])}")
    print(f"len filtered peaks {len(abf['during_stim_peaks'])}")
    return abf


def as_dict(abfd):
    """returns a dictionary with keys `peaks`, `name`, `path`, `sweep`
    to be serialized"""
    out = {}
    out["peaks"] = abfd["during_stim_peaks"].tolist()
    out["name"] = abfd["short_name"]
    out["path"] = abfd["path"]
    out["sweep"] = abfd["sweep"]
    return out
