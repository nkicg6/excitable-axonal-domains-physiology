# utility files for reading and analyzing files
import os

import numpy as np
import scipy.signal as s
import pyabf


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
            "stim_intensity": abf.sweepC,
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
            "stim_intensity": np.asarray([]),
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
