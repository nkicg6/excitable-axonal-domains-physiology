import pathlib
import pytest
import numpy as np

import pyabf


@pytest.fixture()
def good_path_and_map():
    path = str(pathlib.Path("..", "data", "abfs", "20104002.abf").resolve())
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
    path = str(pathlib.Path("..", "not", "real", "thing.abf"))
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
