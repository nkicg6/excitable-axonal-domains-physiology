# analysis for patch clamp current steps analysis
import os
import pyabf
import numpy as np
import scipy.signal as s
import matplotlib.pyplot as plt

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
        print("Using filtered")
        data = abf["filtered"].copy()
        filt_opt = True  # track branch taken
    if not use_filtered:
        print("Not using filtered")
        data = abf["y"].copy()
        filt_opt = False  # track branch taken
    threshold = abs(data.mean() * threshold) + data.mean()
    peaks, props = s.find_peaks(data, height=threshold, distance=11)
    abf["peaks"] = peaks
    abf["peak_props"] = props
    abf["peak_props"]["threshold"] = threshold
    abf["peak_props"]["use_filtered?"] = filt_opt
    return abf


if __name__ == "__main__":
    half_ms_window = 11  # data points for filter
    degree = 3  # based on Mae's paper

    abf = abf_golay(read_abf_IO(cc01test, 5, 0), half_ms_window, degree)
    abf = count_spikes(abf, threshold=0.25, use_filtered=False)
    p = abf["peaks"]

    plt.plot(abf["x"], abf["filtered"])
    plt.plot(abf["x"][p], abf["filtered"][p], ".")
    plt.hlines(y=abf["peak_props"]["threshold"], xmin=abf["x"][0], xmax=abf["x"][-1])
    # filter the data with a golay filter and plot

    plt.show()
