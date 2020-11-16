# add AP features to db
import argparse
import sys
from patch_clamp import database as db
from patch_clamp import ap_analysis as ap


parser = argparse.ArgumentParser(description="add AP features to database")
parser.add_argument("-db", help="path to database")
parser.add_argument("-query", help="Insert query for database")
parser.add_argument("-maxsweep", help="Sweep to target", type=int)
parser.add_argument("-golay", help="Golay window (data point n)", type=int)
parser.add_argument("-mspre", help="ms pre AP", type=int)
parser.add_argument("-mspost", help="ms post AP", type=int)
parser.add_argument("-threshold", help="derivative threshold for spike", type=int)


def main(data):
    for item in data:
        try:
            features = ap.ap_features(
                item, MS_WINDOW_PRE, MS_WINDOW_POST, THRESHOLD, GOLAY_WINDOW
            )
            serialized = ap.serialize_ap_features(features)
            print(f"[INFO] Adding {serialized['fname']} to database...")

            db.add_to_db_parameterized(DB_PATH, INSERT_QUERY, serialized)
        except Exception as e:
            with open("error_log.txt", "a") as er:
                er.write(
                    f"[ERROR]: {item['fpath']}\n[EXCEPTION]: {e}\n[EXCEPTION_TEXT]: {e.__traceback__}\n"
                )
            print(
                f"[Warning] Problem adding {serialized['fname']} to database.\n Exception: \n{e}\n"
            )
            continue
    print("[INFO] Done")


if __name__ == "__main__":
    args = parser.parse_args()
    DB_PATH = args.db
    INSERT_QUERY = args.query
    MAX_SWEEP = args.maxsweep
    MS_WINDOW_PRE = args.mspre
    MS_WINDOW_POST = args.mspost
    THRESHOLD = args.threshold
    GOLAY_WINDOW = args.golay

    # arg list

    for sweep in range(4, MAX_SWEEP):
        print(f"[INFO] Starting sweep {sweep}...")
        DATA_QUERY = ap.QUERY.replace("REPLACEME", str(sweep))
        data = [
            ap.peaks_to_int_list(i) for i in db.sql_data_as_dict(DB_PATH, DATA_QUERY)
        ]
        main(data)
    print("ALL DONE")
