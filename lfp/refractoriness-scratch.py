# analysis for refractoriness
from collections import defaultdict
import os
import numpy as np
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


## template matching
def make_stim_artifact_template(abf, ms_offset):
    """make template for artifact subtraction. Assumes stim channel is 1, and that the first stim is used for the template
    returns a waveform within an offset window containing stim_init:stim_init+ms_offset"""
    abf.setSweep(0, channel=1)
    stims = _find_signal_index(abf.sweepY)
    offset = int(abf.dataPointsPerMs * ms_offset)
    abf.setSweep(0, channel=0)
    return abf.sweepY[stims[0] : stims[0] + offset]


def apply_stim_artifact_template(abf, sweep, ms_offset):
    """returns a trace with a template subtracted at both stim locations for the target sweep"""
    abf.setSweep(sweep, channel=1)
    (stim_one, stim_two) = _find_signal_index(abf.sweepY)
    template = make_stim_artifact_template(abf, ms_offset)
    offset = int(abf.dataPointsPerMs * ms_offset)
    abf.setSweep(sweep, channel=0)
    l_sweep = len(abf.sweepY)
    template_trace = np.zeros(l_sweep)
    template_trace[stim_one : stim_one + offset] = template
    template_trace[stim_two : stim_two + offset] = template
    subtracted = abf.sweepY - template_trace
    return subtracted, template_trace


## testing template matching

sweep = 1
ms_offset = 1
abf = pyabf.ABF(exp_data["199034-1_1_2"][0])

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)

template_subtracted, template_trace = apply_stim_artifact_template(
    abf, sweep, ms_offset
)

abf.setSweep(sweep, channel=0)

ax1.plot(abf.sweepX, abf.sweepY, alpha=0.3, label=f"sweep {sweep}")
ax1.plot(abf.sweepX, template_trace, alpha=0.5, label=f"sweep {sweep} template")
abf.setSweep(10)
ax1.plot(abf.sweepX, abf.sweepY, alpha=0.3, label="sweep 10")

ax2.plot(abf.sweepX, template_subtracted, label=f"sweep {sweep} template subtracted")

ax1.set_xlim([0.5, 0.56])
ax1.set_ylim([-250, 100])
ax1.legend()
ax2.legend()
plt.show()

## we can use this method, but then subtract the single template of the first pulse (~ 9ms past first stim of first sweep) from the *second* stim point. Even neglecting the stimulus artifact subtraction this could work.
