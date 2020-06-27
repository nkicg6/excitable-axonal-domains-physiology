#!/bin/bash
# Run LFP analysis
# must be in venv `lfp`

LFPPATHS=("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-18/"\
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-17"\
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-15"\
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-14"\
         "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-13")

for path in ${LFPPATHS[*]};
do
    python lfp -d $path -a "io"
done
