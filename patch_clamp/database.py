import sqlite3


def make_db(path=None):
    """this is no good get rid of it"""
    if not path:
        con = sqlite3.connect(":memory:")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE testing (short_name TEXT NOT NULL,
        path TEXT NOT NULL,
        sweep INTEGER NOT NULL,
        animal_id TEXT,
        experiment_date TEXT,
        peak_indicies TEXT)"""
        )
    return sqlite3.connect(path)


def list_of_ints_to_str(list_of_ints):
    return ",".join([str(i) for i in list_of_ints])


def str_list_to_list_ints(str_list):
    return [int(i) for i in str_list.split(",")]


if __name__ == "__main__":
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute()
    ld = list_of_dicts[5]

    cursor.execute(
        "INSERT INTO testing (short_name, path, sweep, peak_indicies) VALUES (?, ?, ?, ?)",
        (ld["name"], ld["path"], ld["sweep"], list_of_ints_to_str(ld["peaks"])),
    )
    connection.commit()

    r = cursor.execute("SELECT * FROM testing")
    print(r.fetchall())
    cursor.close()
    connection.close()
