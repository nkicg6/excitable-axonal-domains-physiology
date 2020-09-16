from ephys.patch_clamp import steps


def test_read_abf_IO(good_path_and_map):
    good_path, good_map = good_path_and_map
    sgood = steps.read_abf_IO(good_path, 1, 0)
    assert sgood["path"] == good_path
    assert sgood["sweep"] == 1
    assert sgood["channel"] == 0
    assert sgood["short_name"] == good_map["short_name"]
    assert sgood["error"] == []


def test_bad_read_abf_IO(bad_path_and_map):
    bad_path, bad_map = bad_path_and_map
    sbad = steps.read_abf_IO(bad_path, 1, 0)
    assert sbad["path"] == bad_map["path"]
    assert sbad["sweep"] == 1
    assert sbad["channel"] == 0
    assert sbad["short_name"] == bad_map["short_name"]
    assert len(sbad["x"]) == len(bad_map["x"])
    assert sbad["error"] == [
        "io error: ABF file does not exist: /Users/nick/personal_projects/thesis/thesis_ephys/not/real/thing.abf"
    ]
