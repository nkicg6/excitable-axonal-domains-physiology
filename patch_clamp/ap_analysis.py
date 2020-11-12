from patch_clamp import database as db

QUERY = """SELECT metadata.fname,
           metadata.cell_side,
           metadata.cell_n,
           metadata.treatment_group AS treatment,
           peaks.fpath,
           peaks.peak_index,
           peaks.fpath,
           peaks.sweep
           FROM peaks INNER JOIN metadata
           ON peaks.fname = metadata.fname
           WHERE peaks.sweep = 8"""


def peaks_to_int_list(ditem):
    ditem["peak_index"] = db.str_list_to_list_ints(ditem["peak_index"])
    return ditem
