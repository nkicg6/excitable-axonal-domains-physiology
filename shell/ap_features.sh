# measure AP features, add to db
TABLE_SCHEMA_PATH="/Users/nick/personal_projects/thesis/thesis_ephys/ephys/sql/ap_features.sqlite"
DB_PATH="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
DB_QUERY="INSERT INTO ap_features (fname, fpath, mouse_id, sweep, treatment, cell_side, cell_n, ap_max_voltage, max_dydx, firing_threshold_voltage, ap_amplitude, AHP_amplitude, FWHM) VALUES (:fname, :fpath, :mouse_id, :sweep, :treatment, :cell_side, :cell_n, :ap_max_voltage, :max_dydx, :firing_threshold_voltage, :ap_amplitude, :AHP_amplitude, :FWHM)"
MAXSWEEP=23
GOLAY=25
MSPRE=1
MSPOST=2
THRESHOLD_VOLTS=25


echo "Making table"

python scripts/mk_table.py -db $DB_PATH -schema $TABLE_SCHEMA_PATH

# membrane potential...
python scripts/add_ap_features.py -db $DB_PATH -query "$DB_QUERY" -maxsweep $MAXSWEEP -golay $GOLAY -mspre $MSPRE -mspost $MSPOST -threshold $THRESHOLD_VOLTS
echo "Done!"

