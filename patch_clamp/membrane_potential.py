# measure RMP and add to DB
import numpy as np
import patch_clamp.database as db
import patch_clamp.utils as utils

# Purpose:
# measure the RMP for sweep 0 from each file for cc_01-steps protocol and add it to a
# simple database table with columns fname, fpath, sweep, measured_rmp
# RMP is the mean of the first 0.5s of the sweep.

con = db.persistent_connection_to_db(db.DATABASE_PATH)
con.execute(TABLE)


def get_mean_prestim(abfd, stop_index=10620):
    """takes mean of `filtered` data between 0 and `stop_index`.
    adds this as key `mean_rmp`"""
    m = np.mean(abfd["filtered"][0:stop_index])
    abfd["mean_rmp"] = float(m)
    return abfd


if __name__ == "__main__":
    cc01paths = db.get_paths_for_protocol(db.DATABASE_PATH, "cc_01-steps")
    half_ms_window = 11  # data points for filter
    degree = 3  # based on Mae's paper
    for stepfile in cc01paths:
        abf_file = utils.abf_golay(
            utils.read_abf_IO(stepfile, 0, 0), half_ms_window, degree
        )
        abf_file = get_mean_prestim(abf_file)
        db.add_to_db_parameterized(db.DATABASE_PATH, QUERY, abf_file)
    print("Done")
