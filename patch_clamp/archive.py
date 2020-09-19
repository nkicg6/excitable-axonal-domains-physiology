# add metadata to the patch_metadata.db database
import os
import csv
import sqlite3
import pyabf

SCHEMA_PATH = "schema.sqlite"
# schema names are keys, csv names are values
CSV_TO_SCHEMA_MAP = {
    "fname": "file",
    "fpath": "fpath",  # from matching fname to file list
    "protocol": "protocol",  # from reading file
    "mouse_id": "mouse_id",
    "treatment_group": "treatment_group",
    "experiment_date": "exp_date",
    "sex": "sex",
    "slice_n": "slice_n",
    "cell_n": "cell_n",
    "cell_side": "cell_treatment",
    "ACSF_inhibitors": "ACSF-inhibitors?",
    "surgery_date": "occl_date",
    "bubbles": "bubbles?",
    "genotype": "genotype",
    "fluors": "fluors",
    "filled_cells": "filled_cells?",
    "suspected_cell_type": "susp_cell_type",
    "analysis_to_run": "analysis_to_run",
    "membrane_potential_uncorrected": "membrane_potential_uncorrected",
    "include": "include?",
    "notes": "notes",
}


def get_schema(path):
    """read schema and strip \n, returning a string"""
    with open(path, "r") as schema:
        schema_text = schema.read()
    return schema_text.replace("\n", " ")


def make_db(path, table_schema):
    """creates a SQLite datbase with schema described by string `table_schema`, which
    should be a valid CREATE TABLE sql command. If the table already exists, return the
    connection and cursor objects."""
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        cursor.execute(table_schema)
    except sqlite3.OperationalError as e:
        print(f"Table already exists. Exception is:\n {e}")
        return connection, cursor
    return connection, cursor


def connect_to_db(path):
    """returns the connection to a db which already exists"""
    assert os.path.exists(path)
    assert os.path.isfile(path)
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return connection, cursor


def get_files(base, endswith):
    """returns a sorted list of paths from `base` ending with `endswith`"""
    return sorted(
        [os.path.join(base, i) for i in os.listdir(base) if i.endswith(endswith)]
    )


def files_to_map(file_list):
    return {os.path.split(i)[-1].replace(".abf", ""): i for i in file_list}


def parse_csv(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        stuff = [i for i in reader]
    return stuff


def _read_protocol(abf_path):
    try:
        abf = pyabf.ABF(abf_path)
        return abf.protocol
    except Exception as e:
        print(f"error reading abf {abf_path}. Exception is:\n{e}")
        return f"Error reading: {e}"


def merge_csv_abf_maps(parsed_csv_meta, abf_map):
    parsed_csv_meta = parsed_csv_meta.copy()
    for d in parsed_csv_meta:
        d["fpath"] = abf_map[d["file"]]
        d["protocol"] = _read_protocol(d["fpath"])
    return parsed_csv_meta


def gather_keys(parsed_csv_list):
    out_list = []
    for d in parsed_csv_list:
        temp = {}
        for k in CSV_TO_SCHEMA_MAP.keys():
            temp[k] = d.get(CSV_TO_SCHEMA_MAP[k], "Not found")
        out_list.append(temp)
    return out_list


def insert_db_values(con, cur, metadata):
    items = [
        "fname",
        "fpath",
        "protocol",
        "mouse_id",
        "treatment_group",
        "experiment_date",
        "sex",
        "slice_n",
        "cell_n",
        "cell_side",
        "ACSF_inhibitors",
        "surgery_date",
        "bubbles",
        "genotype",
        "fluors",
        "filled_cells",
        "suspected_cell_type",
        "analysis_to_run",
        "membrane_potential_uncorrected",
        "include",
        "notes",
    ]
    insert_str = f"INSERT INTO metadata ({','.join(items)}) VALUES ({','.join(['?' for i in items])})"
    try:
        cur.execute(insert_str, (metadata[i] for i in items))
        con.commit()
        return 0
    except Exception as e:
        print(f"Problem, exception is:\n {e}")
        return 1


def main(data_path, db_path):
    con, cur = connect_to_db(db_path)
    csv_meta = parse_csv(get_files(data_path, ".csv")[0])
    all_abfs = files_to_map(get_files(data_path, ".abf"))
    merged = merge_csv_abf_maps(csv_meta, all_abfs)
    pass


if __name__ == "__main__":
    main()

target_path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-16"


os.listdir(target_path)
