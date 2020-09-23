# main script for analysis of peaks, records peak times
import sqlite3

import pyabf

import numpy as np
import matplotlib.pyplot as plt

import patch_clamp.database as db

# con = db.persistent_connection_to_db(db.DATABASE_PATH)
# con.row_factory = sqlite3.Row

# this will get all the sweeps, we could also grab all the indexes and compute locations
# in the index where the peak was.
# the simplest thing will be to count the peaks and group with metadata.
# next need to decide whether to group by time bin or something to summarize for raster.


def get_groups_per_sweep(sweep, db_path):
    con = db.persistent_connection_to_db(db_path)
    con.row_factory = sqlite3.Row
    data = con.execute(
        """SELECT
        peaks.peak_index,
        peaks.fname,
        metadata.mouse_id,
        metadata.cell_side,
        metadata.treatment_group,
        metadata.fpath,
        metadata.protocol,
        metadata.cell_n,
        metadata.membrane_potential_uncorrected,
        metadata.include
        FROM peaks INNER JOIN metadata
        ON peaks.fname = metadata.fname
        WHERE peaks.sweep = ? AND include = 'yes'""",
        (sweep,),
    )
    extracted = [
        {
            "fname": p["fname"],
            "fpath": p["fpath"],
            "mouse_id": p["mouse_id"],
            "cell_side": p["cell_side"],
            "cell_n": p["cell_n"],
            "memb_potential": p["membrane_potential_uncorrected"],
            "include": p["include"],
            "protocol": p["protocol"],
            "peaks": p["peak_index"],
            "side": p["cell_side"],
            "treatment": p["treatment_group"],
        }
        for p in data
    ]
    con.close()
    return extracted


def add_real_x(item):
    """fn to map over list of items returned by `get_groups_per_sweep`"""
    i_res = item.copy()
    abf = pyabf.ABF(item["fpath"])
    time = abf.sweepX
    peak_ints = db.str_list_to_list_ints(item["peaks"])
    i_res["peak_times"] = time[peak_ints]
    return i_res


dtest = get_groups_per_sweep(4, db.DATABASE_PATH)
add_real_x(dtest[3])


def serialize(item):
    out = []
    for spike in item["peak_times"]:
        out.append(
            {
                "fname": item["fname"],
                "peak_time": float(spike),
                "mouse_id": item["mouse_id"],
                "cell_side": item["cell_side"],
                "cell_n": item["cell_n"],
                "memb_potential": item["memb_potential"],
                "include": item["include"],
                "protocol": item["protocol"],
                "treatment": item["treatment"],
            }
        )
    if not out:
        return [
            {
                "fname": item["fname"],
                "peak_time": None,
                "mouse_id": item["mouse_id"],
                "cell_side": item["cell_side"],
                "cell_n": item["cell_n"],
                "memb_potential": item["memb_potential"],
                "include": item["include"],
                "protocol": item["protocol"],
                "treatment": item["treatment"],
            }
        ]
    return out


serialized = [serialize(add_real_x(d)) for d in dtest]
serialized_flat = [item for sublist in serialized for item in sublist]


def return_flat_list_of_treatment(dict_of_groups, treatment):
    try:
        abf = pyabf.ABF(dict_of_groups[0]["fpath"])
        time = abf.sweepX
    except TypeError as e:
        print(f"ERROR! \n {dict_of_groups}\n")
    target = [
        db.str_list_to_list_ints(peaks["peaks"])
        for peaks in dict_of_groups
        if peaks["treatment"] == treatment
    ]
    empty_less = [i for i in target if i]
    flat = [item for sublist in empty_less for item in sublist]
    x_time = time[flat]
    return x_time, flat


def count_peaks_treatments(data_dict, treatment):
    target = [
        db.str_list_to_list_ints(peaks["peaks"])
        for peaks in data_dict
        if peaks["treatment"] == treatment
    ]
    n_cells = len(target)
    n_spikes = [len(i) for i in target]
    mean_spikes = np.mean(n_spikes)
    sd_spikes = np.std(n_spikes)
    return {
        "treatment": treatment,
        "n_cells": n_cells,
        "n_spikes": n_spikes,
        "mean_spikes": mean_spikes,
        "sd_spikes": sd_spikes,
    }


sham_count_arr = []
sham_spike_hist_arr = []
occl_count_arr = []
occl_spike_hist_arr = []
paths = []
for sweep in range(23):
    data = get_groups_per_sweep(sweep, db.DATABASE_PATH)
    p = [pp["fpath"] for pp in data]
    paths.append(p)
    count_data = count_peaks_treatments(data, "sham")
    count_data["sweep"] = sweep
    occl_count_data = count_peaks_treatments(data, "occl")
    occl_count_data["sweep"] = sweep
    sham_count_arr.append(count_data)
    occl_count_arr.append(occl_count_data)
    x, _ = return_flat_list_of_treatment(data, "sham")
    xoccl, _ = return_flat_list_of_treatment(data, "occl")
    sham_spike_hist_arr.append(x)
    occl_spike_hist_arr.append(xoccl)


d2 = get_groups_per_sweep(3, db.DATABASE_PATH)
x_ctrl, _ = return_flat_list_of_treatment(d2, "sham")
x_occl, _ = return_flat_list_of_treatment(d2, "occl")

n_bins = 35
fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, sharex=ax1, sharey=ax1)

ax1.hist(x_ctrl, bins=n_bins, color="grey")

ax2.hist(x_occl, bins=n_bins, color="magenta")

plt.show()

fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 1, 1)
for i in sham_count_arr:
    ax1.plot(i["sweep"], i["mean_spikes"], "b.")
for i in occl_count_arr:
    ax1.plot(i["sweep"], i["mean_spikes"], "r.")
plt.show()


fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 1, 1)
for i in sham_count_arr:
    ax1.plot(i["sweep"], i["sd_spikes"], "b.")
for i in occl_count_arr:
    ax1.plot(i["sweep"], i["sd_spikes"], "r.")
plt.show()


fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, sharex=ax1, sharey=ax1)
for n, arr in enumerate(sham_spike_hist_arr):
    ax1.plot(arr, [n for i in arr], ".")
for n, arr in enumerate(occl_spike_hist_arr):
    ax2.plot(arr, [n for i in arr], ".")
plt.show()
