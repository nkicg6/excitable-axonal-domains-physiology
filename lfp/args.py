# command line options and parsing
import argparse

parser = argparse.ArgumentParser(description="Extracellular recording data analysis")

parser.add_argument(
    "-d",
    "--data-directory",
    dest="data_directory",
    help="Directory with data and metadata files",
)
parser.add_argument(
    "-a",
    "--analysis-type",
    dest="analysis_type",
    help="type of analyis to run. Currently supported options include: 'io' ",
)
