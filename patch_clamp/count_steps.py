import patch_clamp.steps as steps
import patch_clamp.database as db
import patch_clamp.archive as archive

SCHEMA = archive.get_schema("patch_clamp/peaks_schema2.sqlite")
con, cur = archive.make_db(db.DATABASE_PATH, SCHEMA)
cur.close()
con.close()


QUERY_STRING = "INSERT INTO peaks (fname, fpath, sweep, peak_index) VALUES (:name, :path, :sweep, :peaks) ON CONFLICT DO NOTHING"
paths = db.get_paths_for_protocol(db.DATABASE_PATH, "cc_01-steps")
HALF_MS_WINDOW = 11
DEGREE = 3
THRESHOLD = 0.8

if __name__ == "__main__":
    for path in paths:
        print(f">>>> analyzing {path}\n\n")
        res = steps.batch_analyze_file(path, HALF_MS_WINDOW, DEGREE, THRESHOLD)
        print(">>>> adding to database")
        for sdict in res:
            db.add_to_db_parameterized(db.DATABASE_PATH, QUERY_STRING, sdict)
        print("\n\n>>>> DONE! <<<<\n\n")
