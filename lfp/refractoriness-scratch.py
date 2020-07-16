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

print(len(exp_data["199034-lear_1_1"]))

for i in exp_data["199034-lear_1_1"]:
    print(i)


def calc_refract_mean(list_of_files, sweep):
    assert (
        len(list_of_files) == 5
    ), f"should be 5 files, but there are {len(list_of_files)}"
    b = []
    for f in list_of_files:
        abf = pyabf.ABF(f)
        abf.setSweep(sweep)
        b.append(abf.sweepY)
    b = np.asarray(b)
    return abf.sweepX, b.mean(axis=0)


x, r = calc_refract_mean(exp_data["199034-lear_1_1"], 1)
plt.plot(x, r)
plt.show()

## now for each sweep I need to find the second stim and use that to get the peaks.
def _find_signal_index(y):
    ind_stim = np.where(y > 1)[0]
    return ind_stim


for i in abf.sweepList:
    abf.setSweep(i, channel=1)
    stim = _find_signal_index(abf.sweepY)
    print(f"sweep {i} is delay: {(stim[1]-stim[0])/ 20}")

sweep = 12
abf = pyabf.ABF(exp_data["199034-1_1_2"][0])
abf.setSweep(sweep, channel=1)
stim = _find_signal_index(abf.sweepY)[1]
offset = int(abf.dataPointsPerMs * 0.5) + stim
abf.setSweep(sweep, channel=0)

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111)
ax1.plot(abf.sweepX, abf.sweepY, alpha=0.3)
ax1.axvline(abf.sweepX[offset], color="green")
ax1.set_xlim([0.5, 0.54])
ax1.set_ylim([-150, 100])
plt.show()

## How can this be factored out to work in production? What am I actually measuring? Can't really do the
## doing an area of the curve may be best... but can't really do that easily?
## try subtracting the first pulse from sweep one (some window, setting the rest to 0 or something), from sweep n, then take the result.
## Could possibly subtract from both? See Tiwari-woodruff
sweep = 10
abf.setSweep(1)
s1 = abf.sweepY.copy()
abf.setSweep(sweep)
s5 = abf.sweepY.copy()

abf.setSweep(sweep, channel=1)
stim = _find_signal_index(abf.sweepY)[0]
offset = int(abf.dataPointsPerMs * 2)  # + stim
sartifact = np.zeros(len(s5))
sartifact[stim - offset : stim + offset] = s5[stim - offset : stim + offset]

abf.setSweep(sweep, channel=0)
fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)

ax1.plot(abf.sweepX, sartifact, alpha=0.3, label="sweep 5")
ax2.plot(abf.sweepX, s5 - sartifact, label="sweep5 minus sweep1")
ax2.plot(abf.sweepX, s5, label="sweep 5")
# ax1.set_xlim([0.5, 0.54])
# ax1.set_ylim([-150, 100])
ax2.legend()
plt.show()

## template matching
def make_template(abf, ms_offset):
    """make template for matching. Assumes stim channel is 1, and that the first stim is used for the template
    returns a waveform within an offset window containing stim_init:stim_init+ms_offset"""
    abf.setSweep(0, channel=1)
    stims = _find_signal_index(abf.sweepY)
    print(f"stims are {stims}")
    offset = int(abf.dataPointsPerMs * ms_offset)
    abf.setSweep(0, channel=0)
    return abf.sweepY[stims[0] : stims[0] + offset]


def apply_template(abf, sweep, ms_offset):
    """returns a trace with a template subtracted at both stim locations for the target sweep"""
    abf.setSweep(sweep, channel=1)
    (stim_one, stim_two) = _find_signal_index(abf.sweepY)
    print(f"stims are {stim_two}")
    template = make_template(abf, ms_offset)
    offset = int(abf.dataPointsPerMs * ms_offset)
    abf.setSweep(sweep, channel=0)
    l_sweep = len(abf.sweepY)
    template_trace = np.zeros(l_sweep)
    template_trace[stim_one : stim_one + offset] = template
    template_trace[stim_two : stim_two + offset] = template
    subtracted = abf.sweepY - template_trace
    return subtracted, template_trace


## testing template matching

sweep = 8
ms_offset = 2
abf = pyabf.ABF(exp_data["199034-1_1_2"][0])

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)

template_subtracted, template_trace = apply_template(abf, sweep, ms_offset)
tmeplate_subtracted, template_first_input = apply_template(abf, sweep, 9)

abf.setSweep(sweep, channel=0)

ax1.plot(abf.sweepX, abf.sweepY, alpha=0.3, label=f"sweep {sweep}")
ax1.plot(abf.sweepX, template_trace, alpha=0.5, label=f"sweep {sweep} template")

ax2.plot(abf.sweepX, template_subtracted, label=f"sweep {sweep} template subtracted")


# ax1.set_xlim([0.5, 0.54])
# ax1.set_ylim([-150, 100])
ax1.legend()
ax2.legend()
plt.show()

## we can use this method, but then subtract the single template of the first pulse (~ 9ms past first stim of first sweep) from the *second* stim point. Even neglecting the stimulus artifact subtraction this could work.


def apply_control_template(abf, sweep):
    """returns a trace with a template subtracted at both stim locations for the target sweep"""
    abf.setSweep(sweep, channel=1)
    (stim_one, stim_two) = _find_signal_index(abf.sweepY)
    print(f"stims are {stim_two}")
    template = make_template(abf, 1)
    offset = int(abf.dataPointsPerMs * 1)
    abf.setSweep(sweep, channel=0)
    l_sweep = len(abf.sweepY)
    template_trace = np.zeros(l_sweep)
    template_trace[stim_two : stim_two + offset] = template
    subtracted = abf.sweepY - template_trace
    return subtracted, template_trace


sweep = 5
ms_offset = 2
abf = pyabf.ABF(exp_data["199034-1_1_2"][0])

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)

template_subtracted, template_trace = apply_control_template(abf, sweep)

abf.setSweep(sweep, channel=0)

ax1.plot(abf.sweepX, abf.sweepY, alpha=0.8, label=f"sweep {sweep}")
abf.setSweep(5)

ax2.plot(abf.sweepX, abf.sweepY, alpha=0.8, label=f"sweep {sweep}")
plt.show()

ax1.plot(abf.sweepX, template_trace, alpha=0.5, label=f"sweep {sweep} template")

ax2.plot(abf.sweepX, template_subtracted, label=f"sweep {sweep} template subtracted")


# ax1.set_xlim([0.5, 0.54])
# ax1.set_ylim([-150, 100])
ax1.legend()
ax2.legend()
plt.show()
