"""parsing operations for LFP analysis.
IO analysis
-----------
json_data = IO_parse_json_main('path/to/datadir')
csv_data = IO_parse_csv_main('path/to/datadir', 'io')
merged = merge_csv_json(csv_data, json_data)
datastructure = make_io_analysis_datastructure(merged)
"""

import csv
import json
import os


# CSV related functions
def _IO_parse_csv(path: str) -> dict:
    outlist = []
    with open(path, "r") as stuff:
        reader = csv.DictReader(stuff)
        for rowdict in reader:
            outlist.append(rowdict)

    return {item["Fname-ref"].strip(".abf"): item for item in outlist}


def _filter_protocol(indict: dict, use_ref_case: str) -> dict:
    prot_filtered = {}
    for k in indict.keys():
        if indict[k]["Use-case-ref"] == use_ref_case:
            prot_filtered[k] = indict[k]
    return prot_filtered


def _add_unique_id(indict: dict) -> dict:
    for item in indict.keys():
        animal = indict[item]["Animal-ref"]
        slice_ = indict[item]["Slice-ref"]
        repref = indict[item]["Rep-ref"]
        unique = "_".join([animal, slice_, repref])
        indict[item]["uniqueid"] = unique
    return indict


# JSON parsing functions
def _IO_get_json_data(base: str, endswith: str) -> list:
    return sorted(
        [os.path.join(base, f) for f in os.listdir(base) if f.endswith(endswith)]
    )


def _IO_return_data(flist: list) -> list:
    good = []
    for i in flist:
        with open(i, "r") as f:
            d = json.load(f)
            good.append(d)
    return good


def _jsonlist_to_dict(jsonlist: list) -> dict:
    return {item["short_filename"]: item for item in jsonlist}


def _IO_get_csv(path: str):
    for p in os.listdir(path):
        if p.endswith(".csv"):
            return os.path.join(path, p)
    return None


def IO_parse_json_main(path: str, endswith: str) -> dict:
    jfiles = _IO_get_json_data(path, endswith)
    jlist = _IO_return_data(jfiles)
    todict = _jsonlist_to_dict(jlist)
    return todict


def merge_csv_json(csv_dict: dict, json_data: dict) -> dict:
    new_d = {}
    for k in csv_dict.keys():
        try:
            new_d[k] = {**csv_dict[k], **json_data[k]}
        except KeyError:
            pass
    return new_d


def IO_parse_csv_main(path: str, protocol: str) -> dict:
    target_csv = _IO_get_csv(path)
    early_parse = _IO_parse_csv(target_csv)
    filtered = _filter_protocol(early_parse, protocol)
    with_id = _add_unique_id(filtered)
    return with_id


def _make_keys_iodict(datadict: dict) -> dict:
    unique = set()
    for k in datadict.keys():
        unique.add(datadict[k]["uniqueid"])
    return {i: {"metadata": [], "io": []} for i in unique}


def make_io_analysis_datastructure(datadict: dict) -> dict:
    iodict = _make_keys_iodict(datadict)
    _get_key = lambda uniqueid: datadict[k][uniqueid]
    for k in datadict.keys():
        fname = _get_key("full_path")
        io = float(_get_key("stim"))
        uid = _get_key("uniqueid")
        start_ind = _get_key("start_ind")
        stop_ind = _get_key("stop_ind")
        use_opt = _get_key("use_opt")
        peak_direction = _get_key("peak_direction")
        animal_ref = _get_key("Animal-ref")
        slice_ref = _get_key("Slice-ref")
        side_ref = _get_key("Side-ref")
        type_ref = _get_key("Type-ref")
        rep_ref = _get_key("Rep-ref")
        iodict[uid]["metadata"].append(datadict[k])
        iodict[uid]["io"].append(
            {
                "unique_id": uid,
                "animal_ref": animal_ref,
                "side_ref": side_ref,
                "type_ref": type_ref,
                "rep_ref": rep_ref,
                "slice_ref": slice_ref,
                "stim": io,
                "file": fname,
                "start_ind": start_ind,
                "stop_ind": stop_ind,
                "use_opt": use_opt,
                "peak_direction": peak_direction,
            }
        )
    for k in iodict.keys():
        iodict[k]["io"].sort(key=lambda iod: iod["stim"])  # sort in place
    return iodict
