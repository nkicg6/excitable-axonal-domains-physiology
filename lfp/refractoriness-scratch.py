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
