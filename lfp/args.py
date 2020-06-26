# command line options and parsing
import argparse
import os

parser = argparse.ArgumentParser(description="Extracellular recording data analysis")

parser.add_argument(
    "-d",
    "--data-directory",
    dest="data_directory",
    required=True,
    help="Directory with data and metadata files",
)
parser.add_argument(
    "-a",
    "--analysis-type",
    dest="analysis_type",
    required=True,
    help="type of analyis to run. Currently supported options include: 'io' ",
)

# TODO!
def validate_args(parser):

    pass
