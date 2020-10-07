library(dplyr)
library(jsonlite)
library(tidyr)
library(ggplot2)

SAVEALL <- FALSE
source("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/figures/2020_04_paper_draft_figures/plotting_defaults/ggplot_theme_defaults.R")
data_paths <- list.files("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001", pattern = "*.json", full.names = T)

res <- bind_rows(purrr::map(data_paths, fromJSON)) %>%
  filter(cell_side != "Open-CHECK") %>%
  mutate(uid = paste(mouse_id, cell_n, sep = "_"))

res$treatment <- forcats::fct_relevel(res$treatment, c("sham", "occl"))
res$cell_side <- forcats::fct_relevel(res$cell_side, c("left", "right", "open", "occl"))



filter(res, sweep == 10) %>%
  ggplot(aes(x = peak_time, color = treatment)) +
  geom_histogram(aes(y = ..density..), fill = "white") +
  facet_grid(~treatment) +
  control_vs_occl_color

res %>%
  group_by(treatment, fname, mouse_id, cell_side, cell_n, sweep) %>%
  summarize(first_peak = min(peak_time)) %>%
  group_by(treatment, mouse_id, cell_side, sweep) %>%
  summarize(fp = mean(first_peak)) %>%
  ggplot(aes(x = cell_side, y = fp)) +
  geom_boxplot() +
  facet_grid(~sweep)

res %>%
  group_by(treatment, fname, mouse_id, cell_side, cell_n, sweep) %>%
  summarize(first_peak = min(peak_time)) %>%
  # filter(sweep == 8) %>%
  ggplot(aes(x = cell_side, y = first_peak)) +
  geom_boxplot() +
  geom_jitter() +
  facet_grid(~sweep)
