
# based on the peaks table, make a new table with spike times
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

# run script once for yes once for maybe
echo "$DB_QUERY"
echo "done"
