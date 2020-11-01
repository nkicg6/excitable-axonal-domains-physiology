# test file for extracting spike times and writing them to a DB
import sqlite3
import patch_clamp.serialize_spike_times as s
import patch_clamp.database as db


def test_serialize(serialize_data_with_peaks):
    data, _ = serialize_data_with_peaks
    val = s.serialize(data)
    vals = [i["peak_time"] for i in val]
    assert vals == [3.0, 5.0, 7.0]


def test_serialize_no_vals(serialize_data_no_peaks):
    val = s.serialize(serialize_data_no_peaks)
    vals = [i["peak_time"] for i in val]
    assert vals == [None]


def test_to_db_no_peaks(peaks_table_schema, serialize_data_no_peaks, spike_times_db):
    db_path = spike_times_db
    val = s.serialize(serialize_data_no_peaks)
    for info in val:
        with_current = s.add_current(info, s.SWEEP_TO_CURRENT_MAP)
        print(with_current)
        s.to_db(with_current, db_path, s.PEAK_INS_QUERY)
    check_con = sqlite3.connect(db_path)
    check_stuff = check_con.execute("SELECT * FROM peak_times").fetchall()
    assert check_stuff == [()]
