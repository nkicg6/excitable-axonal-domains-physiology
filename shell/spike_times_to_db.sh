# add peak times to database table
DB_SCHEMA_PATH="/Users/nick/personal_projects/thesis/thesis_ephys/ephys/sql/peak_times.sqlite"

DB_PATH="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"

DB_QUERY="SELECT peaks.peak_index, 
                 peaks.fname, 
                 metadata.mouse_id, 
                 metadata.cell_side,
                 metadata.treatment_group, 
                 metadata.fpath, 
                 metadata.protocol,
                 metadata.cell_n, 
                 metadata.membrane_potential_uncorrected, 
                 metadata.include 
                 FROM peaks INNER JOIN metadata 
                 ON peaks.fname = metadata.fname 
                 WHERE peaks.sweep = ? AND metadata.include = ?"
SWEEP_MAX=23

python scripts/mk_table.py -db $DB_PATH -schema $DB_SCHEMA_PATH

# run script once for yes once for maybe

echo "Running yes option"
python scripts/add_peak_times.py -db $DB_PATH -query "$DB_QUERY" -sweeps $SWEEP_MAX -include "yes"
echo "Running maybe option"
python scripts/add_peak_times.py -db $DB_PATH -query "$DB_QUERY" -sweeps $SWEEP_MAX -include "maybe"
echo "Done!"
