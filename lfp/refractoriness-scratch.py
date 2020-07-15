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
