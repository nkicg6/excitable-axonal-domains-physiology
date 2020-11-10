# add resting potential table
import argparse
import os
import sys

import patch_clamp.database as db

parser = argparse.ArgumentParser(
    description="Measure resting membrane potential and add to database"
)
parser.add_argument("-db", help="database path")

if __name__ == "__main__":
    print("[add_resting_potential] Starting...")
    args = parser.parse_args()
    DB_PATH = args.db

    if not os.path.exists(DB_PATH):
        sys.exit(f"database {DB_PATH} doesn't exist. Exiting")
    PATHS = db.get_paths_for_protocol(DB_PATH, "cc_01-steps")
    print(f"Paths: {PATHS}")
    for path in PATHS:
        print(f">>>> Analyzing {path}\n\n")
        # get vals, do work
        print(">>>> Adding to database")
    print("Done")
