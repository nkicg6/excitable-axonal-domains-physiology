# Purpose:
# measure the RMP for sweep 0 from each file for cc_01-steps protocol.
# RMP is the mean of the first 0.5s of the sweep. Sweep ending index is hard coded in
# the `stop_index` parameter of membrane_potential.py

import argparse
import os
import sys

import patch_clamp.database as db
import patch_clamp.membrane_potential as mp

parser = argparse.ArgumentParser(
    description="Measure resting membrane potential and add to database"
)
parser.add_argument("-db", help="database path")
parser.add_argument("-window", help="Half ms window for filter", type=int)
parser.add_argument("-degree", help="Degree for filter", type=int)
parser.add_argument("-query", help="generic string for DB insertion")


if __name__ == "__main__":
    print("[add_resting_potential] Starting...")
    args = parser.parse_args()
    DB_PATH = args.db
    DEGREE = args.degree
    WINDOW = args.window
    QUERY = args.query

    if not os.path.exists(DB_PATH):
        sys.exit(f"database {DB_PATH} doesn't exist. Exiting")
    PATHS = db.get_paths_for_protocol(DB_PATH, "cc_01-steps")
    print(f"Paths: {PATHS}")
    for path in PATHS:
        print(f">>>> Analyzing {path}\n\n")
        current_d = mp.read_and_filter(path, WINDOW, DEGREE)
        abf_file = mp.get_mean_prestim(current_d)  # use default stop index
        print(">>>> Adding to database")
        try:
            db.add_to_db_parameterized(DB_PATH, QUERY, abf_file)
        except Exception as e:
            sys.exit(f"Problem adding to database, quitting. Exception: {e}")
    print("Done")
