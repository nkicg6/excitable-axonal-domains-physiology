# add membrane potential table
TABLE_SCHEMA_PATH="/Users/nick/personal_projects/thesis/thesis_ephys/ephys/sql/rmp_cc01.sqlite"

DB_PATH="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"

DB_QUERY="INSERT INTO RMP_CC01 (fname, fpath, sweep, measured_mean_rmp, measured_median_rmp) VALUES (:short_name, :path, :sweep, :mean_rmp, :median_rmp)"


echo "Making table"

python scripts/mk_table.py -db $DB_PATH -schema $TABLE_SCHEMA_PATH

# membrane potential...

echo "Done!"
