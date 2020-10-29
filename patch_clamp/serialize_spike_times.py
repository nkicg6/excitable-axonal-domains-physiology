# helper functions to serialize peak times
import sqlite3

import pyabf

import patch_clamp.database as db


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


def get_x(item):
    abf = pyabf.ABF(item["fpath"])
    abf.setSweep(item["sweep"])
    time = abf.sweepX
    item["x"] = time
    return item


def add_real_x(item):
    """fn to map over list of items returned by `get_groups_per_sweep`"""
    i_res = item.copy()
    peak_ints = db.str_list_to_list_ints(item["peaks"])
    i_res["peak_times"] = i_res["x"][peak_ints]
    return i_res


def serialize(item):
    out = []
    for spike in item["peak_times"]:
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
