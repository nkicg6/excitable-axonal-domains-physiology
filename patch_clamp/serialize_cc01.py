# main script for export of data for R analysis
import json
import sqlite3

import pyabf

import patch_clamp.database as db

DB_QUERY_STRING = """SELECT
        peaks2.peak_index,
        peaks2.fname,
        metadata.mouse_id,
        metadata.cell_side,
        metadata.treatment_group,
        metadata.fpath,
        metadata.protocol,
        metadata.cell_n,
        metadata.membrane_potential_uncorrected,
        metadata.include
        FROM peaks2 INNER JOIN metadata
        ON peaks2.fname = metadata.fname
        WHERE peaks2.sweep = ? AND metadata.include = 'yes'"""

DB_QUERY_STRING_MAYBE = """SELECT
        peaks2.peak_index,
        peaks2.fname,
        metadata.mouse_id,
        metadata.cell_side,
        metadata.treatment_group,
        metadata.fpath,
        metadata.protocol,
        metadata.cell_n,
        metadata.membrane_potential_uncorrected,
        metadata.include
        FROM peaks2 INNER JOIN metadata
        ON peaks2.fname = metadata.fname
        WHERE peaks2.sweep = ? AND metadata.include = 'maybe'"""


def get_groups_per_sweep(sweep, query, db_path):
    con = db.persistent_connection_to_db(db_path)
    con.row_factory = sqlite3.Row
    data = con.execute(query, (sweep,))
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
            "sweep": sweep,
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
                "sweep": item["sweep"],
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
                "sweep": item["sweep"],
            }
        ]
    return out


def write_json(data, path):
    with open(path, "w") as outfile:
        json.dump(data, outfile)


for sweep in range(23):
    p = f"/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/spike_times_sweep_{sweep}_MAYBE_higher_threshold.json"
    sweepdata = get_groups_per_sweep(sweep, DB_QUERY_STRING, db.DATABASE_PATH)
    serialized = [serialize(add_real_x(d)) for d in sweepdata]
    serialized_flat = [item for sublist in serialized for item in sublist]
    write_json(serialized_flat, p)
    print(f"wrote {p}")
