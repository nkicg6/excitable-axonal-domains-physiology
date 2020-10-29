#! /bin/sh
# update metadata
PATHS=("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2019-12-29"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2019-12-30"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-01"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-02"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-03"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-04"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-15"\
           "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/passive_membrane_properties_2020-01-16")

DB_PATH="/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db"
DB_SCHEMA_PATH="/Users/nick/personal_projects/thesis/thesis_ephys/ephys/sql/schema.sqlite"

python scripts/mk_table.py -db $DB_PATH -schema $DB_SCHEMA_PATH
for val in ${PATHS[*]};
do
    python patch_clamp/archive.py -db $DB_PATH -dir $val
done                             
echo "done!"
