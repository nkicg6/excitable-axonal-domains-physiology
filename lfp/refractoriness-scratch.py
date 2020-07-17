# analysis for refractoriness
from collections import defaultdict
import os
import numpy as np
from scipy import signal
import pyabf
import matplotlib.pyplot as plt

from lfp import parsing

##
path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-19/"
abfs = sorted([os.path.join(path, p) for p in os.listdir(path) if p.endswith(".abf")])

##

csv_data = parsing.IO_parse_csv_main(path, "Refract-exp")
exp_data = parsing.make_refractory_dict(path, csv_data)

##


def calc_refract_mean(list_of_files, sweep, channel=0):
    if not list_of_files:
        print(f"[calc_refract_mean] list_of_files is None, exiting")
    assert (
        len(list_of_files) == 5
    ), f"should be 5 files, but there are {len(list_of_files)}"
    b = []
    for f in list_of_files:
        abf = pyabf.ABF(f)
        abf.setSweep(sweep, channel=channel)
        b.append(abf.sweepY)
    b = np.asarray(b)
    return abf.sweepX, b.mean(axis=0)


## now for each sweep I need to find the second stim and use that to get the peaks.
def _find_signal_index(y):
    ind_stim = np.where(y > 1)[0]
    return ind_stim


def print_stim_times(abf):
    for i in abf.sweepList:
        abf.setSweep(i, channel=1)
        stim = _find_signal_index(abf.sweepY)
        print(f"sweep {i} is delay: {(stim[1]-stim[0])/ 20}")
        return


## testing template matching

sweep = 10
ms_offset = 1.0
abf = pyabf.ABF(exp_data["199034-lear_1_1"][0])

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)

(template_subtracted, template_trace, stims) = apply_stim_artifact_template(
    abf, sweep, ms_offset
)

peaks = find_peak_after_stim(template_subtracted, stims[1])

abf.setSweep(sweep, channel=0)

ax1.plot(abf.sweepX, abf.sweepY, alpha=0.3, label=f"sweep {sweep}")
ax1.plot(abf.sweepX, template_trace, alpha=0.5, label=f"sweep {sweep} template")

ax2.plot(abf.sweepX, template_subtracted, label=f"sweep {sweep} template subtracted")
ax2.axvline(abf.sweepX[stims[1]], color="black")
ax2.plot(abf.sweepX[peaks], abf.sweepY[peaks], "r*")
ax1.set_xlim([0.52, 0.53])
ax1.set_ylim([-350, 100])
ax1.legend()
ax2.legend()
plt.show()


## This method above seems to work well.
## we need to work with the first 16 sweeps (10ms IPI to 2ms IPI).
## Need a function that takes the five files and returns a dict with the following information per sweep:
## - mean y data from channel 0
## - dataPointsPerMs
## - stim_indexes
## should take in a list of files, return the data structure described above


def make_data_structure(files: list, max_sweep: int) -> dict:
    structure = {}
    sample_freq = pyabf.ABF(files[0]).dataPointsPerMs
    for sweep in range(max_sweep + 1):
        x, mean_data = calc_refract_mean(files, sweep, channel=0)
        # greater_500 = np.where(mean_data > 300)[0]
        # less_500 = np.where(mean_data < -500)[0]
        # mean_data[greater_500] = 0
        # mean_data[less_500] = 0
        # mean_data = signal.savgol_filter(mean_data, window_length=21, polyorder=3, mode="constant" )

        _, mean_stim_data = calc_refract_mean(files, sweep, channel=1)
        signal_indicies = _find_signal_index(mean_stim_data)
        assert (
            len(signal_indicies) == 2
        ), f"signal indicies {signal_indicies} is incorrect!"
        # signal_indicies = signal_indicies-2 # TESTING HACK
        structure[f"sweep_{sweep}"] = {
            "x": x,
            "y": mean_data,
            "stim_indicies": signal_indicies,
            "ms_sample_rate": sample_freq,
        }
    return structure


def apply_artifat_template(data_struct: dict, ms_offset: float = 2):
    ds = data_struct.copy()
    offset = int(
        ds["sweep_0"]["ms_sample_rate"] * ms_offset
    )  # assumes all offsets within data_struct are equal
    l_sweep = len(ds["sweep_0"]["y"])
    template_acc = []
    for k in ds.keys():
        stim_one, stim_two = ds[k]["stim_indicies"]
        # y_template[stim_one : stim_one + offset] = template
        template = ds[k]["y"][stim_one : stim_one + offset]
        template_acc.append(template)

    template_acc = np.asarray(template_acc)
    template_acc = template_acc.mean(axis=0)
    for k in ds.keys():
        stim_one, stim_two = ds[k]["stim_indicies"]
        y_template = np.zeros(l_sweep)
        y_template[stim_two : stim_two + offset] = template_acc
        subtracted = ds[k]["y"] - y_template
        ds[k]["template"] = y_template
        ds[k]["no_artifact"] = subtracted
        ds[k]["ms_offset"] = ms_offset
    return ds


def _calc_mean_conditioning_amplitude(data_struct: dict, offset_ms=2):
    ds = data_struct.copy()
    stop_offset = int(
        ds["sweep_0"]["stim_indicies"][0] + ds["sweep_0"]["ms_sample_rate"] * offset_ms
    )
    pass


experiment = make_data_structure(exp_data["199034-lear_4_1"], 16)
new_exp = apply_artifat_template(experiment, 3)
##

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111)
# for i in new_exp.keys():
#    ax1.plot(new_exp[i]['x'], new_exp[i]["no_artifact"], label=f"no artifact {i}", alpha=0.4)
sweep = 0
# ax1.plot(
#     new_exp[f"sweep_{sweep}"]["x"],
#     new_exp[f"sweep_{sweep}"]["no_artifact"],
#     label=f"s{sweep} cleaned",
#     alpha=0.4,
# )
ax1.plot(
    new_exp[f"sweep_{sweep}"]["x"],
    new_exp[f"sweep_{sweep}"]["no_artifact"],
    label=f"s{sweep}",
    color="green",
    alpha=0.4,
)
# ax1.plot(
#     new_exp[f"sweep_{sweep}"]["x"],
#     new_exp[f"sweep_{sweep}"]["template"],
#     label=f"template sweep s{sweep}",
#     color="green",
# )

sweep = 6
# ax1.plot(
#     new_exp[f"sweep_{sweep}"]["x"],
#     new_exp[f"sweep_{sweep}"]["no_artifact"],
#     label=f"s{sweep} cleaned",
#     alpha=0.4,
# )
ax1.plot(
    new_exp[f"sweep_{sweep}"]["x"],
    new_exp[f"sweep_{sweep}"]["no_artifact"],
    label=f"s{sweep}",
    color="blue",
    alpha=0.4,
)
# ax1.plot(
#     new_exp[f"sweep_{sweep}"]["x"], new_exp[f"sweep_{sweep}"]["template"], color="blue",
# )

ax1.legend()
# ax1.set_xlim([0.515, 0.535])
plt.show()

for k in exp_data.keys():
    try:
        print(f"key {k} is {exp_data[k][0]}")
    except IndexError:
        print(exp_data[k])
######### This is not working. try just subtracting the
### maybe calculate the mean conditioning pulse for all sweeps. Then use that as the template.
