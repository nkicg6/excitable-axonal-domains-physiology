# play
# https://github.com/pspratt/pyibt
import sqlite3

from patch_clamp import database as db
from patch_clamp import ap_analysis as ap


db_path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
ap_items = [ap.peaks_to_int_list(i) for i in db.sql_data_as_dict(db_path, ap.QUERY)]


peaks = ap.ap_features(ap_items[0], 1, 2, 25)
no_peaks = ap.ap_features(ap_items[1], 1, 2, 25)


def serialize_ap_features(apdict):
    out = {}
    out["fname"] = apdict["fname"]
    out["fpath"] = apdict["fpath"]
    out["mouse_id"] = apdict["mouse_id"]
    out["treatment"] = apdict["treatment"].lower().strip()
    out["cell_side"] = apdict["cell_side"].lower().strip()
    out["cell_n"] = apdict["cell_n"]
    if not apdict["peak_index"]:
        out["ap_max_voltage"] = None
        out["max_dydx"] = None
        out["firing_threshold_voltage"] = None
        out["ap_amplitude"] = None
        out["AHP_amplitude"] = None
        out["FWHM"] = None
        return out
    out["ap_max_voltage"] = float(apdict["ap_max_voltage"][0])
    out["max_dydx"] = float(apdict["max_dydx"][0])
    out["firing_threshold_voltage"] = float(apdict["firing_threshold_voltage"])
    out["ap_amplitude"] = float(apdict["ap_amplitude"])
    out["AHP_amplitude"] = float(apdict["AHP_amplitude"])
    out["FWHM"] = float(apdict["fwhm"][0])
    return out


TEST_DB_PATH = "testdb.db"
QUERY = """INSERT INTO ap_features (fname, fpath, mouse_id, treatment, cell_side, cell_n, ap_max_voltage, max_dydx, firing_threshold_voltage, ap_amplitude, AHP_amplitude, FWHM) VALUES (:fname, :fpath, :mouse_id, :treatment, :cell_side, :cell_n, :ap_max_voltage, :max_dydx, :firing_threshold_voltage, :ap_amplitude, :AHP_amplitude, :FWHM)"""
con = sqlite3.connect(TEST_DB_PATH)
with open("sql/ap_features.sqlite", "r") as f:
    query = f.read().replace("\n", " ")
con.execute(query)
con.commit()
con.close()

s = serialize_ap_features(peaks)
s_no = serialize_ap_features(no_peaks)
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
