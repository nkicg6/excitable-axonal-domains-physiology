# analysis for patch clamp current steps analysis
import numpy as np
import scipy.signal as s

import patch_clamp.database as db
import patch_clamp.utils as utils


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
    try:
        start_x_ind = np.where(abf["x"][abf["peaks"]] > abf["x"][10625])[0][0]
        stop_x_ind = np.where(abf["x"][abf["peaks"]] < abf["x"][30627])[0][-1]
        abf["during_stim_peaks"] = abf["peaks"][start_x_ind:stop_x_ind]
    except IndexError as e:
        print(f"index error:\n {e}")
        abf["during_stim_peaks"] = np.asarray([])
    print(f"len peaks {len(abf['peaks'])}")
    print(f"len filtered peaks {len(abf['during_stim_peaks'])}")
    return abf


def as_dict(abfd):
    """returns a dictionary with keys `peaks`, `name`, `path`, `sweep`
    to be serialized into a database"""
    out = {}
    out["peaks"] = db.list_of_ints_to_str(abfd["during_stim_peaks"].tolist())
    out["name"] = abfd["short_name"]
    out["path"] = abfd["path"]
    out["sweep"] = abfd["sweep"]
    return out


def batch_analyze_file(path, half_ms_window, degree):
    abf = utils.read_abf_IO(path, 0, 0)
    list_of_dicts = []
    for sweep in abf["sweep_list"]:
        abf = utils.abf_golay(utils.read_abf_IO(path, sweep, 0), half_ms_window, degree)
        temp = count_spikes(abf, threshold=0.5, use_filtered=True)
        final = filter_stim_indicies_cc01(temp)
        list_of_dicts.append(as_dict(final))
    return list_of_dicts
