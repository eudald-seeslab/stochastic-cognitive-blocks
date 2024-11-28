# Cognitive Profiles and Social Networks Analysis

This repository contains the code used for the analysis in "Large-scale analysis of the evolving interplay between children's cognitive profiles and social interactions during school years".

## Analysis Sections

### Cognitive Profile Analysis
- `find_optimal_number_of_cognitive_groups.ipynb`: Find the optimal number of both task and student groups.
- `find_cognitive_groups.ipynb`: Implementation of MMSBM for cognitive profile identification with the group number from find_optimal_number_of_cognitive_groups.
- `prediction_power.ipynb`: Comparison of MMSBM with other predictive models
- `figure_2_mmsbm_plots.ipynb`: Visualization of MMSBM results and achievement matrices
- `figure_2_tern_plot.Rmd`: Generation of ternary plots showing student membership distributions
- `figure_2_and_figure_s1_missing_power_comparison_plots`: Comparison between MMSBM achievement and other predictive models
- `figure_s2_plot_hyperopt_cluster_num.ipynb`: Optimization analysis for number of clusters

### Multi-layered Sociogram Analysis 
- `network_funcs.py`: Core functions for social network analysis
- `figure_s3_SBM_Clusters_per_period.ipynb`: Analysis of group structure in sociogram layers
- `figure_3_and_figure_s3_dimensions_correlations.ipynb`: Analysis of overlap between sociogram layers

### Cognitive Profiles and Social Interactions
- `figure_4_adjacent_nodes_distances_random_null_model.ipynb`: Analysis of cognitive profile assortativity
- `figure_5_pr_vs_groups.ipynb`: Analysis of correlation between PageRank and cognitive profiles
- `pr_vs_groups_funcs.py`: Supporting functions for PageRank analysis

### Utility Functions and Configuration
- `plot_funcs.py`: General plotting functions
- `plot_vars.py`: Variable definitions for plotting
- `local_config.yml`: Local configuration parameters

## Requirements
Required Python packages are listed in `requirements.txt`

## Usage Notes
All notebooks contain detailed comments explaining the analysis steps. Start with `find_cognitive_groups.ipynb` to understand the cognitive profile identification process, then follow the sections as they appear in the paper.