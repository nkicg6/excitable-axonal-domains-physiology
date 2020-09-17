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
    assert (
        sbad["error"][0]
        == "io error: ABF file does not exist: /Users/nick/personal_projects/thesis/thesis_ephys/not/real/thing.abf"
    )


def test_golay(good_path_and_map):
    _, good_map = good_path_and_map
    filt = steps.abf_golay(good_map, 11, 3)
    assert filt["savgol_details"] == {"polyorder": 3, "window": 11}
    assert "filtered" in filt.keys()


def test_golay_bad_input(bad_path_and_map):
    _, bad_map = bad_path_and_map
    filt = steps.abf_golay(bad_map, 11, 3)
    assert len(filt["filtered"]) == 0
    assert (
        filt["error"][0]
        == "filter error: If mode is 'interp', window_length must be less than or equal to the size of x."
    )
