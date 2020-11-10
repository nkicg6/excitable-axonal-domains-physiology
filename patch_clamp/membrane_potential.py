# measure RMP and add to DB
import numpy as np
import patch_clamp.utils as utils

# Purpose:

# simple database table with columns fname, fpath, sweep, measured_rmp


def read_and_filter(fpath, half_ms_window, degree):
    abf_file = utils.read_abf_IO(fpath, 0, 0)
    filtered = utils.abf_golay(abf_file, half_ms_window, degree)
    return filtered


def get_mean_prestim(abfd, stop_index=10620):
    """takes mean and median of `filtered` data between 0 and `stop_index`.
    adds this as key `mean_rmp` and `median_rmp`"""
    mean_rmp = np.mean(abfd["filtered"][0:stop_index])
    median_rmp = np.median(abfd["filtered"][0:stop_index])
    abfd["mean_rmp"] = float(mean_rmp)
    abfd["median_rmp"] = float(median_rmp)
    return abfd
