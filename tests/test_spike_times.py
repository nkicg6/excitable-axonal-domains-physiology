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


## Make the database a fixture, setup a 'temp.db' and remove it when the tests are over.
def test_to_db_no_peaks(peaks_table_schema, serialize_data_no_peaks):
    con = sqlite3.connect(":memory:")
    con.execute(peaks_table_schema)
    val = s.serialize(serialize_data_no_peaks)
    for info in val:
        with_current = s.add_current(info, s.SWEEP_TO_CURRENT_MAP)
        s.to_db(with_current, ":memory:", s.PEAK_INS_QUERY)
    stuff = con.execute("SELECT * FROM peak_times").fetchall()
    assert stuff == [()]
