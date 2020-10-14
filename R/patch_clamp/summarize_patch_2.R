library(dplyr)
library(jsonlite)
library(tidyr)
library(ggplot2)

SAVEALL <- FALSE
source("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/figures/2020_04_paper_draft_figures/plotting_defaults/ggplot_theme_defaults.R")
data_paths <- list.files("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001", pattern = "*_higher_threshold.json", full.names = T)


res <- bind_rows(purrr::map(data_paths, fromJSON)) %>%
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
      cell_side == "left" ~ "Left",
      cell_side == "right" ~ "Right",
      cell_side == "open" ~ "Left",
      cell_side == "occl" ~ "Right",
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

res$treatment <- forcats::fct_relevel(res$treatment, c("Control", "Naris Occlusion"))
res$cell_side_comparison <- forcats::fct_relevel(res$cell_side_comparison, c("Left", "Right"))
res$cell_side <- forcats::fct_relevel(res$cell_side, c("Left", "Right", "Open", "Occluded"))
res$three_case <- forcats::fct_relevel(res$three_case, c("Control", "Open", "Occluded"))

count_spikes_df <- res %>%
  group_by(fname, mouse_id, cell_side, cell_n, treatment, sweep) %>%
  summarize(n_peaks = sum(has_peak)) %>%
  group_by(mouse_id, cell_side, cell_n, treatment, sweep) %>%
  summarize(mean_peaks = mean(n_peaks))

count_spikes_three_case_df <- res %>%
  group_by(fname, mouse_id, three_case, cell_n, treatment, sweep) %>%
  summarize(n_peaks = sum(has_peak)) %>%
  group_by(mouse_id, three_case, cell_n, treatment, sweep) %>%
  summarize(mean_peaks = mean(n_peaks))

current_steps <- seq(-0.05, 0.5, 0.025)

glm.three <- glm(mean_peaks ~ sweep * three_case, data = count_spikes_three_case_df, family = poisson(link = "log"))
summary(glm.three)

count_spikes_three_case_df %>%
  ggplot(aes(x = sweep, y = mean_peaks, color = three_case)) +
  geom_smooth() +
  theme_and_axis_legend +
  labs(x = "Current step (pA)", y = "Spike frequency (Hz)") +
  # scale_x_discrete(breaks=current_steps) +
  three_color

ggsave("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/figures/2020_04_paper_draft_figures/patch_clamp_figure/steps.png", width = 8, height = 4, dpi = 300)

# ISI
isi <- res %>%
  group_by(fname, mouse_id, three_case, cell_n, treatment, sweep) %>%
  arrange(peak_time, .by_group = T) %>%
  mutate(ISI = peak_time - lag(peak_time))

isi %>%
  # filter(sweep == 10) %>%
  ggplot(aes(ISI, fill = cell_side)) +
  geom_histogram(binwidth = 0.01) +
  facet_grid(~sweep)

isi %>%
  group_by(sweep, three_case) %>%
  filter(sweep == 10) %>%
  # summarize(mean_isi = mean(ISI, na.rm = T)) %>%
  ggplot(aes(x = factor(sweep), y = ISI, fill = three_case)) +
  geom_violin()
