# parsing opts for LFP analysis
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

    return {item['Fname-ref'].strip(".abf"):item for item in outlist}

def _filter_protocol(indict: dict, use_ref_case: str) -> dict:
    prot_filtered = {}
    for k in indict.keys():
        if indict[k]["Use-case-ref"] == use_ref_case:
            prot_filtered[k] = indict[k]
    return prot_filtered

def _add_unique_id(indict: dict) -> dict:
    for item in indict.keys():
        animal = indict[item]['Animal-ref']
        slice_ = indict[item]['Slice-ref']
        repref = indict[item]['Rep-ref']
        unique = "_".join([animal, slice_, repref])
        indict[item]['uniqueid'] = unique
    return indict

def IO_parse_csv_main(path: str, protocol: str) -> dict:
    early_parse = _IO_parse_csv(path)
    filtered = _filter_protocol(early_parse, protocol)
    with_id = _add_unique_id(filtered)
    return with_id
