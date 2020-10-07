# play with data from ramp experiments
library(dplyr)
library(DBI)
library(ggplot2)

SAVEALL <- FALSE
source("/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/figures/2020_04_paper_draft_figures/plotting_defaults/ggplot_theme_defaults.R")
img_save_rt <- "../../temp"
DB_PATH <- "/Users/nick/Dropbox/lab_notebook/projects_and_data/mnc/analysis_and_data/patch_clamp/data/summary_data/spiking_201912-202001/patch_data.db"
con <- dbConnect(RSQLite::SQLite(), DB_PATH)

query <- "SELECT
ramp.first_peak_stim_intensity,
ramp.fname,
metadata.mouse_id,
metadata.cell_side,
metadata.treatment_group,
metadata.fpath,
metadata.protocol,
metadata.cell_n,
metadata.membrane_potential_uncorrected,
metadata.include
FROM ramp INNER JOIN metadata ON ramp.fname = metadata.fname"

res <- dbGetQuery(con, query) %>%
  filter(cell_side != "Open-CHECK") %>%
  mutate(treatment = case_when(
    treatment_group == "occl" ~ "Naris Occlusion",
    treatment_group == "sham" ~ "Control",
    TRUE ~ "unknown"
  )) %>%
  mutate(side = case_when(
    cell_side == "left" ~ "Left",
    cell_side == "right" ~ "Right",
    cell_side == "open" ~ "Open",
    cell_side == "occl" ~ "Occluded",
    TRUE ~ "unknown"
  ))
dbDisconnect(con)

res$treatment_group <- forcats::fct_relevel(res$treatment, c("Control", "Naris Occlusion"))
res$side <- forcats::fct_relevel(res$side, c("Left", "Right", "Open", "Occluded"))

filter(res, treatment == "Control") %>%
  ggplot(aes(x = side, y = first_peak_stim_intensity, color = side)) +
  geom_boxplot(size = line_size) +
  ctrl_color +
  geom_jitter(size = pt_size, alpha = pt_alpha, width = 0.1) +
  facet_grid(~treatment) +
  labs(y = "Stimulation intensity (nA)", x = "") +
  theme_and_axis_nolegend +
  scale_y_continuous(breaks = c(0.0, 0.1, 0.2, 0.3), limits = c(0, 0.31))
ggsave(file.path(img_save_rt, "control.png"), dpi = 300, height = 6, width = 4)

filter(res, treatment == "Naris Occlusion") %>%
  ggplot(aes(x = side, y = first_peak_stim_intensity, color = side)) +
  geom_boxplot(size = line_size) +
  occl_color +
  geom_jitter(size = pt_size, alpha = pt_alpha, width = 0.1) +
  facet_grid(~treatment) +
  labs(y = "Stimulation intensity (nA)", x = "") +
  theme_and_axis_nolegend +
  scale_y_continuous(breaks = c(0.0, 0.1, 0.2, 0.3), limits = c(0, 0.31))
ggsave(file.path(img_save_rt, "no.png"), dpi = 300, height = 6, width = 4)


fake_data <- data.frame("Prop" = rnorm(20, 0.9, sd = 0.05))
fake_data$treatment <- c(rep("Control"), rep("Naris Occlusion"))
fd_bar <- group_by(fake_data, treatment) %>% summarize(m = mean(Prop))

ggplot(fake_data, aes(x = treatment, y = Prop, color = treatment)) +
  geom_bar(
    inherit.aes = F, aes(x = treatment, y = m, color = treatment), width = barplot_width, size = line_size,
    fill = "white", stat = "identity", data = fd_bar
  ) +
  theme_and_axis_nolegend +
  annotate("text", x = 2.5, y = 0.5, label = "FAKE DATA -- EXAMPLE",
           hjust=1.1, vjust=-1.1, col="grey", cex=8,
           fontface = "bold", alpha = 0.9)+
  geom_jitter(width = 0.15, size = pt_size) +
  labs(x = "", y = "Prop. of cells with complete dend.") +
  control_vs_occl_color
ggsave(file.path(img_save_rt, "fake_morph.png"), dpi = 300, height = 7, width = 6)
