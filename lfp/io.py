# io files for LFP analysis
import os


def io_return_data_endswith(path, endswith):
    """returns sorted list of files from base `path` ending with `endswith`"""
    return sorted(
        [os.path.join(base, f) for f in os.listdir(base) if f.endswith(endswith)]
    )
