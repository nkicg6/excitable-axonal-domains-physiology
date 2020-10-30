import pathlib
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
        "fpath": "/Users/nick/personal_projects/thesis/thesis_ephys/ephys/data/abfs/20104002.abf",
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
    data2 = {
        "fname": "20104003",
        "fpath": "/Users/nick/personal_projects/thesis/thesis_ephys/ephys/data/abfs/20104003.abf",
        "mouse_id": "mid-none",
        "cell_side": "right",
        "cell_n": 2,
        "memb_potential": -65.4,
        "include": "yes",
        "protocol": "cc-01_steps",
        "peaks": [1, 2, 6],
        "x": [1, 2, 3, 4, 5, 6, 7, 8],
        "treatment": "occl",
        "sweep": 5,
    }
    return data1, data2


@pytest.fixture()
def serialize_data_no_peaks():
    data = {
        "fname": "20104005",
        "fpath": "/Users/nick/personal_projects/thesis/thesis_ephys/ephys/data/abfs/20104005.abf",
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
