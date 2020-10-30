# helper functions to serialize peak times
import sqlite3

import pyabf

import patch_clamp.database as db


def get_groups_per_sweep(sweep, query, db_path):
    """pulls out all the data in a sweep and structures it as a dict.
    String of integers (`peaks`) is transformed into a list of ints or empty list."""
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
            "peaks": db.str_list_to_list_ints(p["peak_index"]),
            "treatment": p["treatment_group"],
            "sweep": sweep,
        }
        for p in data
    ]
    con.close()
    return extracted


def get_x(item):
    """adds the x (time) array for the sweep"""
    abf = pyabf.ABF(item["fpath"])
    abf.setSweep(item["sweep"])
    time = abf.sweepX
    item["x"] = time
    return item


def serialize(item):
    out = []
    for spike_ind in item["peaks"]:
        spike = item["x"][spike_ind]
        out.append(
            {
                "fname": item["fname"],
                "fpath": item["fpath"],
                "mouse_id": item["mouse_id"],
                "cell_side": item["cell_side"],
                "cell_n": item["cell_n"],
                "membrane_potential": item["memb_potential"],
                "include": item["include"],
                "protocol": item["protocol"],
                "treatment": item["treatment"],
                "sweep": item["sweep"],
                "peak_time": float(spike),
            }
        )
    if not out:
        return [
            {
                "fname": item["fname"],
                "fpath": item["fpath"],
                "mouse_id": item["mouse_id"],
                "cell_side": item["cell_side"],
                "cell_n": item["cell_n"],
                "membrane_potential": item["memb_potential"],
                "include": item["include"],
                "protocol": item["protocol"],
                "treatment": item["treatment"],
                "sweep": item["sweep"],
                "peak_time": None,
            }
        ]
    return out
