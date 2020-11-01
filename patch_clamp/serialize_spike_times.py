# helper functions to serialize peak times
import sqlite3

import pyabf

import patch_clamp.database as db

PEAK_INS_QUERY = """INSERT INTO peak_times
                    VALUES (:fname, :fpath, :mouse_id, :cell_side, :cell_n,
                            :membrane_potential, :include, :protocol,
                            :treatment, :sweep, :current, :peak_time)"""

SWEEP_TO_CURRENT_MAP = {
    0: -0.05,
    1: -0.025,
    2: 0.0,
    3: 0.025,
    4: 0.05,
    5: 0.075,
    6: 0.1,
    7: 0.125,
    8: 0.15,
    9: 0.175,
    10: 0.2,
    11: 0.225,
    12: 0.25,
    13: 0.275,
    14: 0.3,
    15: 0.325,
    16: 0.35,
    17: 0.375,
    18: 0.4,
    19: 0.425,
    20: 0.45,
    21: 0.475,
    22: 0.5,
}


def get_groups_per_sweep(sweep, include, query, db_path):
    """pulls out all the data in a sweep and structures it as a dict.
    String of integers (`peaks`) is transformed into a list of ints or empty list."""
    con = db.persistent_connection_to_db(db_path)
    con.row_factory = sqlite3.Row
    data = con.execute(query, (sweep, include))
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


def add_current(item):
    try:
        item["current"] = SWEEP_TO_CURRENT_MAP[item["sweep"]]
    except TypeError:
        print(f"type sweep: {type(item['sweep'])}")
        print(f"val sweep: {item['sweep']}")
    return item


def to_db(dict_item, db, query):
    """add dict_item to database (db) using query"""
    try:
        con = sqlite3.connect(db)
        con.execute(query, dict_item)
        con.commit()
    except Exception as e:
        print(f"Exception adding dict to database. Exception is {e}\n.")
        print(f"Dict is {dict_item}")
        print(f"Query is {query}")
    finally:
        con.close()
