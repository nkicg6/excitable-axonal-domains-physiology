import pyabf
import scipy.signal as s
import numpy as np
from patch_clamp import database as db

QUERY = """SELECT metadata.fname,
           metadata.cell_side,
           metadata.cell_n,
           metadata.treatment_group AS treatment,
           peaks.fpath,
           peaks.peak_index,
           peaks.fpath,
           peaks.sweep
           FROM peaks INNER JOIN metadata
           ON peaks.fname = metadata.fname
           WHERE peaks.sweep = 8"""


def peaks_to_int_list(ditem):
    ditem["peak_index"] = db.str_list_to_list_ints(ditem["peak_index"])
    return ditem


def ap_read_filter_derivative(d, ms_window, golay_window_pts=19):
    """returns the dict with keys `ap_x`, `ap_y` representing the
    AP and surrounding window `ms_window`.
    `ms_window` is split in half, and applied around the peak index. For example,
    a 6ms window will be 3ms before the peak and 3 after."""
    ditem = d.copy()
    try:
        first_index = ditem["peak_index"][0]
    except IndexError:
        ditem["ap_x"] = []
        ditem["ap_y"] = []
        ditem["dydx"] = []
        return ditem
    abf = pyabf.ABF(ditem["fpath"])
    abf.setSweep(ditem["sweep"])
    y_filtered = s.savgol_filter(abf.sweepY, golay_window_pts, 3)
    one_sided_pts_around = int((ms_window * abf.dataPointsPerMs) / 2)
    start = first_index - one_sided_pts_around
    stop = first_index + one_sided_pts_around
    ditem["ap_y"] = y_filtered[start:stop]
    ditem["ap_x"] = abf.sweepX[start:stop]
    ditem["dydx"] = (
        np.diff(ditem["ap_y"]) / np.diff(ditem["ap_x"])
    ) / 1000  # to V from mV
    return ditem


def ap_read_filter_derivative(d, ms_window, golay_window_pts=19):
    """returns the dict with keys `ap_x`, `ap_y` representing the
    AP and surrounding window `ms_window`.
    `ms_window` is split in half, and applied around the peak index. For example,
    a 6ms window will be 3ms before the peak and 3 after."""
    ditem = d.copy()
    try:
        first_index = ditem["peak_index"][0]
    except IndexError:
        ditem["ap_x"] = []
        ditem["ap_y"] = []
        ditem["dydx"] = []
        return ditem
    abf = pyabf.ABF(ditem["fpath"])
    abf.setSweep(ditem["sweep"])
    y_filtered = s.savgol_filter(abf.sweepY, golay_window_pts, 3)
    one_sided_pts_around = int((ms_window * abf.dataPointsPerMs) / 2)
    start = first_index - one_sided_pts_around
    stop = first_index + one_sided_pts_around
    ditem["ap_y"] = y_filtered[start:stop]
    ditem["ap_x"] = abf.sweepX[start:stop]
    ditem["dydx"] = (
        np.diff(ditem["ap_y"]) / np.diff(ditem["ap_x"])
    ) / 1000  # to V from mV
    return ditem


def ap_read_filter_derivative(d, ms_window, golay_window_pts=19):
    """returns the dict with keys `ap_x`, `ap_y` representing the
    AP and surrounding window `ms_window`.
    `ms_window` is split in half, and applied around the peak index. For example,
    a 6ms window will be 3ms before the peak and 3 after."""
    ditem = d.copy()
    try:
        first_index = ditem["peak_index"][0]
    except IndexError:
        ditem["ap_x"] = []
        ditem["ap_y"] = []
        ditem["dydx"] = []
        return ditem
    abf = pyabf.ABF(ditem["fpath"])
    abf.setSweep(ditem["sweep"])
    y_filtered = s.savgol_filter(abf.sweepY, golay_window_pts, 3)
    one_sided_pts_around = int((ms_window * abf.dataPointsPerMs) / 2)
    start = first_index - one_sided_pts_around
    stop = first_index + one_sided_pts_around
    ditem["ap_y"] = y_filtered[start:stop]
    ditem["ap_x"] = abf.sweepX[start:stop]
    ditem["dydx"] = (
        np.diff(ditem["ap_y"]) / np.diff(ditem["ap_x"])
    ) / 1000  # to V from mV
    return ditem


def ap_read_filter_derivative(d, ms_window, golay_window_pts=19):
    """returns the dict with keys `ap_x`, `ap_y` representing the
    AP and surrounding window `ms_window`.
    `ms_window` is split in half, and applied around the peak index. For example,
    a 6ms window will be 3ms before the peak and 3 after."""
    ditem = d.copy()
    try:
        first_index = ditem["peak_index"][0]
    except IndexError:
        ditem["ap_x"] = []
        ditem["ap_y"] = []
        ditem["dydx"] = []
        return ditem
    abf = pyabf.ABF(ditem["fpath"])
    abf.setSweep(ditem["sweep"])
    y_filtered = s.savgol_filter(abf.sweepY, golay_window_pts, 3)
    one_sided_pts_around = int((ms_window * abf.dataPointsPerMs) / 2)
    start = first_index - one_sided_pts_around
    stop = first_index + one_sided_pts_around
    ditem["ap_y"] = y_filtered[start:stop]
    ditem["ap_x"] = abf.sweepX[start:stop]
    ditem["dydx"] = (
        np.diff(ditem["ap_y"]) / np.diff(ditem["ap_x"])
    ) / 1000  # to V from mV
    return ditem
