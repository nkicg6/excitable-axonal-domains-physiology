library(dplyr)
library(jsonlite)
library(tidyr)
library(DBI)

data_paths <- list.files("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001",
                         pattern = "*_higher_threshold.json", full.names = T)

spikes_table <- bind_rows(purrr::map(data_paths, fromJSON)) %>%
  filter(cell_side != "Open-CHECK") %>%
  mutate(
    uid = paste(fname, mouse_id, cell_side, cell_n, treatment, sep = "_"),
    group_id = paste(mouse_id, cell_side, cell_n, treatment, sep = "_"),
    treatment = case_when(
      treatment == "sham" ~ "Control",
      treatment == "occl" ~ "Naris Occlusion",
      TRUE ~ "Unknown"
    ),
    cell_side = case_when(
      cell_side == "left" ~ "Left",
      cell_side == "right" ~ "Right",
      cell_side == "open" ~ "Open",
      cell_side == "occl" ~ "Occluded",
      TRUE ~ "Unknown"
    ),
    cell_side_comparison = case_when(
      cell_side == "Left" ~ "Left",
      cell_side == "Right" ~ "Right",
      cell_side == "Open" ~ "Left",
      cell_side == "Occluded" ~ "Right",
      TRUE ~ "Unknown"
    ),
    has_peak = case_when(
      !is.na(peak_time) ~ 1,
      is.na(peak_time) ~ 0
    ),

    three_case = case_when(
      treatment == "Control" ~ "Control",
      cell_side == "Occluded" ~ "Occluded",
      cell_side == "Open" ~ "Open",
      TRUE ~ "Unknown"
    ),
    current = case_when(
      sweep == 0 ~ -0.05,
      sweep == 1 ~ -0.025,
      sweep == 2 ~ 0.0,
      sweep == 3 ~ 0.025,
      sweep == 4 ~ 0.05,
      sweep == 5 ~ 0.075,
      sweep == 6 ~ 0.1,
      sweep == 7 ~ 0.125,
      sweep == 8 ~ 0.15,
      sweep == 9 ~ 0.175,
      sweep == 10 ~ 0.2,
      sweep == 11 ~ 0.225,
      sweep == 12 ~ 0.25,
      sweep == 13 ~ 0.275,
      sweep == 14 ~ 0.3,
      sweep == 15 ~ 0.325,
      sweep == 16 ~ 0.35,
      sweep == 17 ~ 0.375,
      sweep == 18 ~ 0.4,
      sweep == 19 ~ 0.425,
      sweep == 20 ~ 0.45,
      sweep == 21 ~ 0.475,
      sweep == 22 ~ 0.5
    )
  )

spikes_table$treatment <- forcats::fct_relevel(spikes_table$treatment, c("Control", "Naris Occlusion"))
spikes_table$cell_side_comparison <- forcats::fct_relevel(spikes_table$cell_side_comparison, c("Left", "Right"))
spikes_table$cell_side <- forcats::fct_relevel(spikes_table$cell_side, c("Left", "Right", "Open", "Occluded"))
spikes_table$three_case <- forcats::fct_relevel(spikes_table$three_case, c("Control", "Open", "Occluded"))

DB_PATH <- "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data.db"

con <- dbConnect(RSQLite::SQLite(), DB_PATH)
dbWriteTable(con, "steps_table", spikes_table, row.names = F)
