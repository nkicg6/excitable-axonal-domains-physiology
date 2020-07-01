## Summarize LFP analysis
library(dplyr)
library(ggplot2)
library(jsonlite)

data_dirs <- c("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-19/",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-18/",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-17",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-15",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-14",
               "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/extracellular_lfp/data/2020-03-13")

read_and_fmt_json <- function(path){
  jsonfiles = jsonlite::fromJSON(path) %>%
    mutate(amplitude = as.numeric(amplitude))
}

io_file_from_json <- function(pathvector){
  json_files = list.files(pathvector, pattern = "_io_results.json", full.names = T)
  exclude_file_path = list.files(pathvector, pattern="exclude.json", full.names = T)
  exclude_file = jsonlite::fromJSON(exclude_file_path)
  print(exclude_file_path)
  purrr::map(json_files, read_and_fmt_json) %>%
    bind_rows() %>%
    anti_join(.,exclude_file, by=c("unique_id"="exclude"))
}


all_files <- bind_rows(purrr::map(data_dirs, io_file_from_json)) %>% filter(stim <= 1) #%>% filter(use_opt!="Maybe")

ggplot(all_files, aes(x=stim, y=amplitude, color=side_ref))+
  geom_smooth()+
  facet_grid(~type_ref)

ggplot(all_files, aes(x=stim, y=amplitude, color=type_ref))+
  geom_smooth()

all_files %>%
  group_by(animal_ref, type_ref, side_ref, slice_ref, stim) %>%
  summarize(amp_mean = mean(amplitude)) %>%
  group_by(type_ref, side_ref, stim) %>%
  summarize(amp_type_mean = mean(amp_mean), amp_sd = sd(amp_mean), n = n()) %>% View()

all_files %>%
  group_by(animal_ref, type_ref, side_ref, slice_ref, stim) %>%
  summarize(amp_mean = mean(amplitude)) %>%
  ggplot(aes(x=stim, y=amp_mean, color=side_ref))+
  geom_point()+
  facet_grid(~type_ref)
