"""Creates database table with a defined schema if it does not already exist."""
import argparse
import os
import sys
import sqlite3


def get_schema(path):
    """read schema and strip \n, returning a single line string"""
    with open(path, "r") as schema:
        schema_text = schema.read()
    return schema_text.replace("\n", " ")


# Setup parser

parser = argparse.ArgumentParser(
    description="Create database table if it does not already exist."
)
parser.add_argument("-db", help="full path to a valid database")
parser.add_argument("-schema", help="full path to a schema file")

# script

args = parser.parse_args()

if not os.path.exists(args.schema):
    sys.exit(f"Schema file {args.schema} does not exist.")

schema = get_schema(args.schema)
con = sqlite3.connect(args.db)
try:
    con.execute(schema)
except Exception as e:
    print(f"Something went wrong. Exception:\n {e}")

sys.exit("Table created")
