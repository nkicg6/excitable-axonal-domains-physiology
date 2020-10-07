import numpy as np
import scipy.signal as s
import patch_clamp.database as db

QUERY_STRING = "INSERT INTO ramp (fname, fpath, sweep, peak_indicies_array, stim_intensities_at_peak_array, first_peak_stim_intensity) VALUES (:fname, :fpath, :sweep, :peak_indicies_array, :stim_intensities_at_peak_array, :first_peak_stim_intensity) ON CONFLICT DO NOTHING"


def get_ramps_from_db():
    con = db.persistent_connection_to_db(db.DATABASE_PATH)
    paths = con.execute(
        "SELECT fpath FROM metadata WHERE protocol = 'cc_03-rheobase' AND include = 'yes'"
    ).fetchall()
    p = [i[0] for i in paths]
    con.close()
    return p


def find_ramp_peaks(abfd):
    abf = abfd.copy()
    assert abf["protocol"] == "cc_03-rheobase"
    peaks, pead_dict = s.find_peaks(abf["filtered"], height=0, distance=11)
    if not peaks.size:
        abf["peak_indicies"] = np.asarray([])
        abf["stim_intensities_at_peak_array"] = np.asarray([])
        abf["first_peak_stim_intensity"] = None
        return abf
    abf["peak_indicies"] = peaks
    abf["stim_intensities_at_peak_array"] = abf["stim_intensity"][peaks]
    abf["first_peak_stim_intensity"] = abf["stim_intensities_at_peak_array"][0]
    return abf


def serialize_for_db(abfd):
    out = {}
    out["fname"] = abfd["short_name"]
    out["fpath"] = abfd["path"]
    out["sweep"] = abfd["sweep"]
    out["peak_indicies_array"] = db.list_of_ints_to_str(abfd["peak_indicies"])
    out["stim_intensities_at_peak_array"] = db.list_of_floats_to_str(
        abfd["stim_intensities_at_peak_array"]
    )
    out["first_peak_stim_intensity"] = abfd["first_peak_stim_intensity"]
    return out


def add_to_db(con, serialized_dict):

    try:
        con.execute(QUERY_STRING, serialized_dict)
        con.commit()
        return 0
    except Exception as e:
        print(f"Error with serialized_dict:\n {serialized_dict}")
        print(f"\nError is {e}")
        return 1


# 1. make new DB to hold this data
# 2. Serialize for DB fn
# 3. iterate through all files (and sweeps? how many sweeps?)
# 4. add data to DB
# 5. write fn to merge with metadata
# 6. analyze in R
