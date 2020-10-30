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
    data = serialize_data_no_peaks
    val = s.serialize(data)
    vals = [i["peak_time"] for i in val]
    assert vals == [None]
