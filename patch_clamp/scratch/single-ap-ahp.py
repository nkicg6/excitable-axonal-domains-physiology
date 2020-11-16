# play
# https://github.com/pspratt/pyibt
import sqlite3

from patch_clamp import database as db
from patch_clamp import ap_analysis as ap


db_path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"

sweep = 8

QUERY2 = ap.QUERY.replace("REPLACEME", str(sweep))
ap_items = [ap.peaks_to_int_list(i) for i in db.sql_data_as_dict(db_path, QUERY2)]


peaks = ap.ap_features(ap_items[0], 1, 2, 25)
no_peaks = ap.ap_features(ap_items[1], 1, 2, 25)


TEST_DB_PATH = "testdb.db"
QUERY = """INSERT INTO ap_features (fname, fpath, mouse_id, sweep, treatment, cell_side, cell_n, ap_max_voltage, max_dydx, firing_threshold_voltage, ap_amplitude, AHP_amplitude, FWHM) VALUES (:fname, :fpath, :mouse_id, :sweep, :treatment, :cell_side, :cell_n, :ap_max_voltage, :max_dydx, :firing_threshold_voltage, :ap_amplitude, :AHP_amplitude, :FWHM)"""
con = sqlite3.connect(TEST_DB_PATH)
with open("sql/ap_features.sqlite", "r") as f:
    query = f.read().replace("\n", " ")
con.execute(query)
con.commit()
con.close()

s = ap.serialize_ap_features(peaks)
s_no = ap.serialize_ap_features(no_peaks)
print(">>>> Adding to database")

##
try:
    db.add_to_db_parameterized(TEST_DB_PATH, QUERY, s)
    db.add_to_db_parameterized(TEST_DB_PATH, QUERY, s_no)
except Exception as e:
    print(f"Problem adding to database, quitting. Exception: {e}")
print("Done")


"""
for item in ap_items:
    current = ap.ap_features(item, 1, 2, 25)
    f = ap.plot_ap_features(current)
    plt.show()
    print("NEXT")
"""
