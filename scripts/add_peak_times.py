import argparse
import patch_clamp.serialize_spike_times as s

parser = argparse.ArgumentParser(description="add peak times to the database")
parser.add_argument("-query", help="Insert query for database")
parser.add_argument("-sweeps", help="Max sweeps", type=int)
parser.add_argument("-db", help="Database path")
parser.add_argument("-include", help="`yes` or `maybe` for database include")
parser.add_argument(
    "-dry_run",
    help="if present, write to STDOUT, else, write to the database",
    action="store_true",
)


if __name__ == "__main__":

    args = parser.parse_args()
    SWEEP_MAX = args.sweeps
    QUERY = args.query
    DB_PATH = args.db
    INCLUDE = args.include

    for sweep in range(SWEEP_MAX):
        sweepdata = s.get_groups_per_sweep(sweep, INCLUDE, QUERY, DB_PATH)
        all_d = map(s.get_x, sweepdata)
        for f in all_d:
            serialized = s.serialize(f)
            for item in serialized:
                item = s.add_current(item)
                if args.dry_run:
                    print(item)
                if not args.dry_run:
                    s.to_db(item, DB_PATH, s.PEAK_INS_QUERY)
