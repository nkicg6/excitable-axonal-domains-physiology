import os
import numpy as np
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
