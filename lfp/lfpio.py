import os
import pyabf
import matplotlib.pyplot as plt
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

    if len(peak_ind) < 1:
        peak_y = np.array([])
        peak_x = np.array([])
        return {
            "peak_subset_index": peak_ind,
            "peak_x_val": peak_x,
            "peak_y_val": peak_y,
            "peak_dict": peak_dict,
        }
    if len(peak_ind) > 1:
        # hack to return as an array
        peak_ind = int(peak_ind[0])
        peak_y = np.asarray([y_subset[peak_ind]])
        peak_x = np.asarray([x_subset[peak_ind]])
        return {
            "peak_subset_index": peak_ind,
            "peak_x_val": peak_x,
            "peak_y_val": peak_y,
            "peak_dict": peak_dict,
        }
    if len(peak_ind) == 1:
        peak_y = y_subset[peak_ind]
        peak_x = x_subset[peak_ind]
        return {
            "peak_subset_index": peak_ind,
            "peak_x_val": peak_x,
            "peak_y_val": peak_y,
            "peak_dict": peak_dict,
        }


def _get_amplitude(peak_y_val, baseline_y):
    if peak_y_val.size == 1:
        return abs(baseline_y - peak_y_val)
    if peak_y_val.size > 1:
        return abs(baseline_y - peak_y_val[0])
    if peak_y_val.size < 1:
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


def _make_io_img_path(basepath, title):
    p = os.path.join(basepath, title)
    p = p + "_io_experiment.png"
    return p


def input_output_experiment_plot(result_input_output_experiment: list, title: str):
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_title(title)
    for experiment in result_input_output_experiment:
        basepath, id_title = os.path.split(experiment["file"])
        peakind = experiment["peak_results_dict"]["peak_subset_index"]
        ax1.plot(experiment["subset_x"], experiment["subset_y"])
        ax1.plot(
            experiment["subset_x"][peakind],
            experiment["subset_y"][peakind],
            marker="*",
            markersize=15,
        )
        ax2.plot(
            experiment["stim"],
            experiment["amplitude"],
            marker=".",
            markersize=15,
            label=id_title,
        )
    savepath = _make_io_img_path(basepath, title)
    ax2.legend()
    fig.savefig(savepath)
    print(f"saving to {savepath}")


def _list_to_none_or_val(l):
    if not l:
        return None
    if len(l) == 1:
        return l[0]
    if len(l) != 0:
        return "ERROR"


def _np_array_to_float_or_list(d):
    result = {}
    for k in d.keys():
        if isinstance(d[k], np.ndarray):
            result[k] = _list_to_none_or_val(d[k].tolist())
        else:
            result[k] = d[k]
    return result


def gather_io_data_to_json(data):
    result = []
    for io_entry in data:
        exp_data = io_entry.copy()
        peak_results = exp_data.pop("peak_results_dict").copy()
        peak_dict = peak_results.pop("peak_dict")
        exp_data.pop("subset_x")
        exp_data.pop("subset_y")
        res = {**peak_results, **exp_data, **peak_dict}
        result.append(_np_array_to_float_or_list(res))
    return result
