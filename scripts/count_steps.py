import argparse
import os
import sys

import patch_clamp.steps as steps
import patch_clamp.database as db


paths = db.get_paths_for_protocol(db.DATABASE_PATH, "cc_01-steps")

parser = argparse.ArgumentParser(description="count spikes and record indicies")
parser.add_argument("-db", help="database path")
parser.add_argument("-window", help="Half ms window for filter")
parser.add_argument("-degree", help="Degree for filter")
parser.add_argument("-query", help="generic string for DB insertion")

if __name__ == "__main__":
    args = parser.parse_args()
    HALF_MS_WINDOW = args.window
    DEGREE = args.degree
    THRESHOLD = args.threshold
    DB_PATH = args.db
    QUERY = args.query
    if not os.path.exists(DB_PATH):
        sys.exit(f"database {DB_PATH} doesn't exist. Exiting")
    PATHS = db.get_paths_for_protocol(DB_PATH, "cc_01-steps")

    for path in PATHS:
        print(f">>>> analyzing {path}\n\n")
        res = steps.batch_analyze_file(path, HALF_MS_WINDOW, DEGREE, THRESHOLD)
        print(">>>> adding to database")
        for sdict in res:
            db.add_to_db_parameterized(DB_PATH, QUERY, sdict)
        print("\n\n>>>> DONE! <<<<\n\n")
