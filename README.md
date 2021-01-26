# Code used for electrophysiology in my PhD project

Initial submission date: 2021-01-25 

bioRxiv link: https://www.biorxiv.org/content/10.1101/2021.01.25.428132v1

See [excitable-axonal-domains-figures](https://github.com/nkicg6/excitable-axonal-domains-figures) for code used to generate figures and analyze data. 

Analysis code for physiology section of my thesis project. Please note the code and instructions were developed on macOS Mojave (version `10.14.6`) with a GNU bash shell (version `3.2.57(1)`), Python (version `3.7-3.9`), and sqlite3 (version `3.24.0`).

# Notes on staying organized

Preventing spaghetti code and remembering how things are done is very important! It is amazing how quickly I forget how some analysis was done, or what files were included. 

We use scripting languages to perform data analysis so that our research is reproducible. However, most analysis is actually an analysis pipeline. Often I am re-running an analysis with different parameters, or different input files, and this often leads to copying the main script file with new hard-coded inputs, or commenting and re-assigning global input variables (e.g. new paths for new data). Which analysis led to which output? Which is most recent? What exactly were the input files? 

Here is a somewhat ugly method I have settled on to document code runs:

1. Analysis is developed using `*_scratch` files.
1. Once I have the basic analysis worked out, I try to factor useful functions into a library (`patch_clamp` in this case).
1. I will write a write a batch script (with a `main()`) that lives in `scripts/`.
1. The batch script will take command line inputs (a path list and any parameters) and won't have many hard-coded variables.
1. Batch files will then be run with shell scripts. 
1. Shell script changes are tracked with git.

The goal of this workflow is to accomodate common code change and allow me to track different analysis runs. So batches can be re-run with different parameters using a shell script, which documents exactly what was done, what the outputs were, and allows it to be re-run.

# Creating new shell scripts

Scripts will be run from the base of this repository. Ensure you are in the `patch` virtualenv (`pip install .` from this repository's root) before you run a script. Write the shell script, then run `chmod +x <script-name>` to make executable. 

Scripts can then be run via `shell/<script-name.sh>`

# Spikes analysis key and notes

- Database path is `/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data_batch.db`
- `update_metadata_db.sh` adds the metadata to the database
- `spikes.sh` will be the main driver adding the peaks to the database
  - Most recent run was with git hash: **1b61c2d**
- `spike_times_to_db.sh` adds peak times to a structured table for ISI analysis and peak counting
  - Most recent run was with git hash: **d6b9e22**
- `membrane_potential.sh` adds resting membrane potential (mean and median) to the database
  - Most recent run was with git hash: **a323557**
- `action_potential.sh` adds action potential features to the database
  - Most recent run was with git hash: **fdaeb4f**

# Tests

Tests can be run with `pytest .` if the package is installed via `pip`.   
