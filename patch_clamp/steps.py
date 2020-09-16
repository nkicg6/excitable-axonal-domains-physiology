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
            "error": [f"io error: {e}"],
        }


def abf_golay(abfd, window=11, polyorder=3):
    abf = abfd.copy()
    try:
        filtered = s.savgol_filter(abf["y"], polyorder=polyorder, window_length=window)
    except ValueError as e:
        filtered = np.asarray([])
        abf["error"].append(f"filter error: {e}")
    abf["filtered"] = filtered
    abf["savgol_details"] = {"polyorder": polyorder, "window": window}
    return abf


half_ms_window = 11  # data points for filter
degree = 3  # based on Mae's paper

# abf = abf_golay(read_abf_IO(cc01test, 5, 0), half_ms_window, degree)
# print("test")
# plt.plot(abf["x"], abf["filtered"])
# # plt.plot(
# #     abf.sweepX,
# #     s.savgol_filter(abf.sweepY, polyorder=degree, window_length=half_ms_window),
# #     color="red",
# # )
# # filter the data with a golay filter and plot


# plt.show()
