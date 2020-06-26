import pyabf
import numpy as np
import scipy.signal as s


def _IO_calc_mean_io_trace(path):
    abf = pyabf.ABF(path)
    l = []
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        l.append(abf.sweepY)
    l = np.asarray(l)
    return abf.sweepX, l.mean(axis=0)


def _mean_baseline_150ms(mean_sweep):
    return np.mean(mean_sweep[:3000])


def _make_subsets(x, y, start, stop):
    subset_x = x[start:stop]
    subset_y = y[start:stop]
    return subset_x, subset_y


def _find_peak(x_subset, y_subset, peak_direction):
    if peak_direction == "-":
        direction = -1
    if peak_direction == "+":
        direction = 1
    peak_ind, peak_dict = s.find_peaks(
        direction * y_subset, distance=10, prominence=5, width=10, height=20
    )
    if len(peak_ind) != 1:
        peak_y = np.array([])
        peak_x = np.array([])
        print(f"No or multiple peaks found, peaks = {peak_ind}")
    else:
        peak_y = y_subset[peak_ind]
        peak_x = x_subset[peak_ind]

    return {
        "peak_subset_index": peak_ind,
        "peak_x_val": peak_x,
        "peak_y_val": peak_y,
        "peak_dict": peak_dict,
    }


def _get_amplitude(peak_y_val, baseline_y):
    if not len(peak_y_val) == 0:
        return baseline_y - peak_y_val
    else:
        return 0


def _fmt_results_dict(amplitude, subset_x, subset_y, peak_results, entry):
    return {
        "amplitude": amplitude,
        "subset_x": subset_x,
        "subset_y": subset_y,
        "peak_results_dict": peak_results,
        **entry,
    }


def _input_output_single_entry(entry_dict):
    """entry dict to io results dict"""
    x, y = _IO_calc_mean_io_trace(entry_dict["file"])
    baseline = _mean_baseline_150ms(y)
    subset_x, subset_y = _make_subsets(
        x, y, entry_dict["start_ind"], entry_dict["stop_ind"]
    )
    peak_results = _find_peak(subset_x, subset_y, entry_dict["peak_direction"])
    amplitude = _get_amplitude(peak_results["peak_y_val"], baseline)
    return _fmt_results_dict(amplitude, subset_x, subset_y, peak_results, entry_dict)


def input_output_experiment(io_list: list) -> list:
    result = []
    for io_entry in io_list:
        temp_result = _input_output_single_entry(io_entry)
        result.append(temp_result)
    return result
