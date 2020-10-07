# serialize data for ramp experiment
import json
import sqlite3

import patch_clamp.database as db


def get_groups_per_sweep(sweep, db_path):
    con = db.persistent_connection_to_db(db_path)
    con.row_factory = sqlite3.Row
    data = con.execute(
        """SELECT
        ramp.first_peak_stim_intensity,
        ramp.fname,
        metadata.mouse_id,
        metadata.cell_side,
        metadata.treatment_group,
        metadata.fpath,
        metadata.protocol,
        metadata.cell_n,
        metadata.membrane_potential_uncorrected,
        metadata.include
        FROM ramp INNER JOIN metadata
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
            "sweep": sweep,
        }
        for p in data
    ]
    con.close()
    return extracted
