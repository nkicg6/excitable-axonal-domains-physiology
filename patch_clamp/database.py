import sqlite3


DATABASE_PATH = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"


def persistent_connection_to_db(path):
    """returns a connection object for the `path` to a database"""
    return sqlite3.connect(path)


def add_to_db(path, query_string):
    """uses a context manager to open a connection to database at `path` and execute
    query in `query_string`. Returns a 0 for success or a 1 for failure."""
    try:
        con = sqlite3.connect(path)
        with con:
            con.execute(query_string)
        con.close()
        return 0
    except Exception as e:
        print(f"Failed to execute. Query: {query_string}\n with error:\n{e}")
        con.close()
        return 1


def add_to_db_parameterized(path, query_string, data):
    """uses a context manager to open a connection to database at `path` and execute
    query in `query_string`. Returns a 0 for success or a 1 for failure."""
    try:
        con = sqlite3.connect(path)
        with con:
            con.execute(query_string, data)
        con.close()
        return 0
    except Exception as e:
        print(f"Failed to execute. Query: {query_string}\n with error:\n{e}")
        con.close()
        return 1


def get_paths_for_protocol(path_to_db, prot):
    """returns a list of paths from metadata which matching the protocol `prot` and
    `include` is `yes` or `maybe`"""
    query = "SELECT fpath FROM metadata WHERE protocol = ? AND (include = 'yes' OR include = 'maybe')"
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        with con:
            things = con.execute(query, (prot,)).fetchall()
        con.close()
        return sorted([s["fpath"] for s in things])
    except Exception as e:
        print(f"Failed to execute. Query: {query}\n with error:\n{e}")
        con.close()
        return 1


def sql_data_as_dict(path_to_db: str, select_query: str) -> list:
    """Returns data from an query as a list of dicts."""
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        things = con.execute(select_query).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()


def list_of_ints_to_str(list_of_ints):
    return ",".join([str(i) for i in list_of_ints])


def list_of_floats_to_str(list_of_floats):
    return ",".join([str(i) for i in list_of_floats])


def str_list_to_list_floats(str_list):
    if not str_list:
        return []
    return [float(i) for i in str_list.split(",")]


def str_list_to_list_ints(str_list):
    if not str_list:
        return []
    return [int(i) for i in str_list.split(",")]
