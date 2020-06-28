## Summarize LFP analysis
library(dplyr)
library(jsonlite)

data_dirs <- c("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-19/",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-18/",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-17",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-15",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-14",
         "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-13")


