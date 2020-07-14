# analysis for refractoriness
from collections import defaultdict
import os
import numpy as np
import pyabf
import matplotlib.pyplot as plt

from lfp import parsing
##
path ="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-19/"
abfs = sorted([os.path.join(path, p) for p in os.listdir(path) if p.endswith(".abf")])


##
abf = pyabf.ABF(abfs[21])
plt.plot(abf.sweepX, abf.sweepY)
plt.show()

##

def mean_refractory_experiment(path_list, sweep):
    b = []
    for p in path_list:
        abf = pyabf.ABF(p)
        abf.setSweep(sweep)
        b.append(abf.sweepY)
    b = np.asarray(b)
    return b.mean(axis=0)

exp_targets = [21,22, 23, 24, 25]
exp_paths = [abfs[i] for i in exp_targets]

s1 = mean_refractory_experiment(exp_paths, 1)
##

fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(111)

for f in exp_paths:
    abf = pyabf.ABF(f)
    abf.setSweep(1)
    ax1.plot(abf.sweepX, abf.sweepY, alpha=0.5)
ax1.plot(abf.sweepX, s1, linewidth=2, label="mean")
plt.show()

##
csv_parsed = parsing.IO_parse_csv_main(path, "Refract-exp")
print(csv_parsed.keys())
##

def make_refractory_dict(base: str, d: dict) -> dict:
    """returns a dictionary containing all refractory experiments broken down by unique id (key) and a list of 5 paths"""
    newd = defaultdict(list)
    for k in d.keys():
        uid = d[k]['uniqueid']
        p = os.path.join(base, d[k]['Fname-ref'])
        assert os.path.exists(p), f"path {p} does not exist."
        newd[uid].append(p)
    return newd

dd = make_keys_refract(path,csv_parsed)
print(dd['199034-lear_4_2'])
##
