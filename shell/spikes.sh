#!/bin/bash
# count peaks add them to db
# vars
DB_PATH="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
DB_SCHEMA_PATH="/Users/nick/personal_projects/thesis/thesis_ephys/ephys/sql/peaks_schema.sqlite"
HALF_MS_WINDOW=11
DEGREE=3
THRESHOLD=0.8
QUERY_STRING="INSERT INTO peaks (fname, fpath, sweep, peak_index) VALUES (:name, :path, :sweep, :peaks) ON CONFLICT DO NOTHING"

# main script, first make DB and table

python scripts/mk_table.py -db $DB_PATH -schema $DB_SCHEMA_PATH
python scripts/count_steps.py -db $DB_PATH -window $HALF_MS_WINDOW -degree $DEGREE -threshold $THRESHOLD -query $QUERY_STRING

echo "done"

