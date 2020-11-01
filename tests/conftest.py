import os
import pathlib
import sqlite3
import pytest
import numpy as np

import pyabf


@pytest.fixture()
def good_path_and_map():
    path = str(pathlib.Path("data", "abfs", "20104002.abf").resolve())
    abf = pyabf.ABF(path)
    abf.setSweep(sweepNumber=1, channel=0)
    good = {
        "path": path,
        "sweep": 1,
        "channel": 0,
        "x": abf.sweepX,
        "y": abf.sweepY,
        "short_name": "20104002",
        "error": [],
    }
    return path, good


@pytest.fixture()
def bad_path_and_map():
    path = str(pathlib.Path("not", "real", "thing.abf"))
    bad = {
        "path": path,
        "sweep": 1,
        "channel": 0,
        "x": np.asarray([]),
        "y": np.asarray([]),
        "short_name": "thing",
        "error": [],
    }
    return path, bad


@pytest.fixture()
def serialize_data_with_peaks():
    data1 = {
        "fname": "20104002",
        "fpath": "abfs/20104002.abf",
        "mouse_id": "mid-none",
        "cell_side": "left",
        "cell_n": 2,
        "memb_potential": -65.5,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [2, 4, 6],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    return data1


@pytest.fixture()
def serialize_data_no_peaks():
    data = {
        "fname": "20104005",
        "fpath": "abfs/20104005.abf",
        "mouse_id": "mid-none",
        "cell_side": "right",
        "cell_n": 2,
        "memb_potential": -65.4,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    return data


@pytest.fixture()
def serialize_data_duplicate_peaks():
    data = {
        "fname": "20104005",
        "fpath": "abfs/20104005.abf",
        "mouse_id": "mid-none",
        "cell_side": "right",
        "cell_n": 2,
        "memb_potential": -65.4,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [1, 1],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    return data


@pytest.fixture()
def serialize_data_duplicate_peaks_diff_files():
    data = {
        "fname": "20104005",
        "fpath": "abfs/20104005.abf",
        "mouse_id": "mid-none",
        "cell_side": "right",
        "cell_n": 2,
        "memb_potential": -65.4,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [1, 2],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    data2 = {
        "fname": "20104006",
        "fpath": "abfs/20104006.abf",
        "mouse_id": "mid-none",
        "cell_side": "right",
        "cell_n": 2,
        "memb_potential": -65.4,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [1, 2],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    return [data, data2]


@pytest.fixture()
def peaks_table_schema():
    with open("sql/peak_times.sqlite", "r") as schema_file:
        schema = schema_file.read().replace("\n", " ")
    return schema


@pytest.fixture()
def spike_times_db(tmpdir):
    db = str(tmpdir / "test_spikes.db")
    # setup db for testing spike_times insertions
    with open("sql/peak_times.sqlite", "r") as schema_f:
        schema = schema_f.read().replace("\n", " ")
    con = sqlite3.connect(db)
    con.execute(schema)
    yield db
    con.close()
    os.remove(db)
