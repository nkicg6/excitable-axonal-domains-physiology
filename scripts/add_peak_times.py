import argparse
import patch_clamp.serialize_spike_times as pt

parser = argparse.ArgumentParser(description="add peak times to the database")
parser.add_argument("-query", help="Insert query for database")
parser.add_argument("-sweeps", help="Max sweeps", type=int)
parser.add_argument("-db", help="Database path")


if __name__ == "__main__":

    args = parser.parse_args()
    SWEEP_MAX = args.sweeps
    QUERY = args.query
    DB_PATH = args.db

    for sweep in range(23):
        sweepdata = pt.get_groups_per_sweep(sweep, DB_QUERY_STRING, db.DATABASE_PATH)
        serialized = [serialize(add_real_x(d)) for d in sweepdata]
        serialized_flat = [item for sublist in serialized for item in sublist]
        write_json(serialized_flat, p)
