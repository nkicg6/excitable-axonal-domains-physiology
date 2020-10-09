import matplotlib.pyplot as plt
import patch_clamp.steps as steps
import patch_clamp.utils as utils
import patch_clamp.database as db

cc01paths = db.get_paths_for_protocol(db.DATABASE_PATH, "cc_01-steps")
target = cc01paths[50]
# to measure:
# - time of each spike for each step in a dict where the keys are the sweeps and the
#   values are the spike times
# Then, I can write this out to disc and do the calculations later.
# TODO:
# - make the fn to compose and build the dict to serialize to disc
# - use the previously written function to find all the CC01 files to use.
# - must bin by 1/2 ms or something and calculate spike or not spike in each 1/2 ms.
# That's how you build the raster. But first, just write the spike times out
# record all spike times. build raster plots.
# see p 31 of theoretical neuroscience
# then, start binning the data, and calculate the mean and variance for each bin.


half_ms_window = 11  # data points for filter
degree = 3  # based on Mae's paper

target = cc01paths[5]  # 5 sweep 10 is weird
##
##
abf_file = utils.abf_golay(utils.read_abf_IO(target, 22, 0), half_ms_window, degree)
# abf = steps.filter_stim_indicies_cc01(
#     steps.count_spikes(abf, threshold=1, use_filtered=True)
# )
abf = steps.filter_stim_indicies_cc01(
    steps.count_spikes_simple_threshold(abf_file, use_filtered=True)
)
abf_v = steps.filter_stim_indicies_cc01(
    steps.count_spikes(abf_file, threshold=0.8, use_filtered=True)
)
p = abf["peaks"]
p2 = abf["during_stim_peaks"]

plt.plot(abf["x"], abf["filtered"])
plt.plot(abf["x"][p], abf["filtered"][p], ".")
try:
    plt.plot(abf["x"][p2], abf["filtered"][p2], "*")
except IndexError:
    pass

plt.hlines(y=abf["peak_props"]["threshold"], xmin=abf["x"][0], xmax=abf["x"][-1])
plt.hlines(
    y=abf_v["peak_props"]["threshold"],
    xmin=abf_v["x"][0],
    xmax=abf_v["x"][-1],
    color="red",
)
plt.vlines(x=abf["x"][10625], ymin=-80, ymax=30, color="red")
plt.vlines(x=abf["x"][30624], ymin=-80, ymax=30, color="red")
plt.show()


##
##
list_of_dicts = []
for sweep in abf["sweep_list"]:
    abf = utils.abf_golay(utils.read_abf_IO(target, sweep, 0), half_ms_window, degree)
    temp = steps.count_spikes(abf, threshold=0.5, use_filtered=True)
    abf = steps.filter_stim_indicies_cc01(temp)
    list_of_dicts.append(steps.as_dict(abf))
    plt.plot(abf["during_stim_peaks"], [sweep for i in abf["during_stim_peaks"]], ".")
plt.show()

plt.plot(abf["x"], abf["filtered"])
plt.plot(abf["x"][p], abf["filtered"][p], ".")
plt.plot(abf["x"][p2], abf["filtered"][p2], "*")
plt.hlines(y=abf["peak_props"]["threshold"], xmin=abf["x"][0], xmax=abf["x"][-1])
