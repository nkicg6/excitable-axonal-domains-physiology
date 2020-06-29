## Summarize LFP analysis
library(dplyr)
library(jsonlite)

data_dirs <- c("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-19/",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-18/",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-17",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-15",
              "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-14",
         "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-13")


of_files <- purrr::map(data_dirs, list.files(pattern="_io_results.json", full.names=T))
allFiles <- list.files(data_dirs[1], pattern = "_io_results.json", full.names = T)

io_file_from_json <- function(pathvector){
  json_files = list.files(pathvector, pattern = "_io_results.json", full.names = T)
  read_in = purrr::map(json_files, jsonlite::fromJSON)
  return(bind_rows(read_in))
}

io_file_from_json(data_dirs[1])
