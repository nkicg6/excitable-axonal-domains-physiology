# play
# https://github.com/pspratt/pyibt


import matplotlib.pyplot as plt

from patch_clamp import database as db
from patch_clamp import ap_analysis as ap


db_path = "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
ap_items = [ap.peaks_to_int_list(i) for i in db.sql_data_as_dict(db_path, ap.QUERY)]


## Look at all

for item in ap_items:
    current = ap.ap_features(item, 1, 2, 25)
    f = ap.plot_ap_features(current)
    plt.show()
    print("NEXT")
