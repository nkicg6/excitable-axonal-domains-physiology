# main script for analysis of peaks, records peak times

import patch_clamp.archive as archive
import patch_clamp.database as db
import patch_clamp.steps as steps

SCHEMA = archive.get_schema("patch_clamp/peaks_schema.sqlite")
con, cur = archive.make_db(db.DATABASE_PATH, SCHEMA)
cur.close()
con.close()

QUERY_STRING = "INSERT INTO peaks (fname, fpath, sweep, peak_index) VALUES (:name, :path, :sweep, :peaks) ON CONFLICT DO NOTHING"
cc01paths = db.get_paths_for_protocol(db.DATABASE_PATH, "cc_01-steps")
HALF_MS_WINDOW = 11  # data points for filter
DEGREE = 3  # based on Mae's paper

if __name__ == "__main__":
    for path in cc01paths:
        print(f">>>> analyzing {path}\n\n")
        res = steps.batch_analyze_file(path, HALF_MS_WINDOW, DEGREE)
        print(">>>> adding to database")
        for sdict in res:
            db.add_to_db_parameterized(db.DATABASE_PATH, QUERY_STRING, sdict)
