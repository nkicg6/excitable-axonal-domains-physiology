# Code used for PhD project

Analysis code for physiology section of my thesis project

# Notes on staying organized

Preventing spaghetti code and remembering how things are done is of utmost importance. It is amazing how quickly I forget how some analysis was done, or what files were included. 

We use scripting languages to perform serious data analysis, and we have the benefit of reproducible research (ability to re-run the analysis and get the same result). However, this benefit is only automatic for simple scripts. Often I am re-running an analysis with different parameters, or different input files, and this often leads to copying the main script file with new hard-coded inputs, or commenting and re-assigning global input variables. Which analysis led to which output? Which is most recent? What exactly were the input files? 

Here is a somewhat ugly method I have settled on to document code runs:

1. Analysis is developed using `*_scratch` files.
2. Once I have it worked out, the library functions go in a file under `patch_clamp` or `lfp` and I write a batch function that lives in `scripts/`.
3. The batch file will take command line inputs. So a path list, and any parameters.
4. Batch files will then be run with shell scripts. 

The idea is that batches can be re-run with different parameters using a shell script, which documents exactly what was done, what the outputs were, and allows it to be re-run.

# Creating new shell scripts

Scripts will be run from `ephys/`, and this becomes the working directory. Ensure you are in the `patch` virtualenv before you run a script. Write the shell script, then run `chmod +x <script-name>` to make executable. 

Scripts can then be run via `shell/<script-name.sh>`

# spikes analysis

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
