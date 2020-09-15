# analysis for patch clamp current steps analysis
import pyabf
import numpy as np
import scipy.signal as s
import matplotlib.pyplot as plt

cc01test = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-04/20104002.abf"

abf = pyabf.ABF(cc01test)

abf.setSweep(15)
plt.plot(abf.sweepX, abf.sweepY)
plt.show()
