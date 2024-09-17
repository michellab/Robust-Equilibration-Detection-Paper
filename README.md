# Robust-Equilibration-Detection-Paper

Inputs and code to reproduce the results and analysis from "Robust Equilibration Detection for Molecular Simulations". Analysis is performed using the [RED](https://github.com/fjclark/red) package.

```
├── analysis
│   ├── analysis_free.ipynb
│   ├── analysis.ipynb
│   └── analysis_single.ipynb
├── compute_equil_times
│   ├── compute_equil_times.py
│   └── compute_equil_times.sh
└── synthetic_data_creation
    ├── dataset_creation.ipynb
    ├── dataset_creation_free.ipynb
    └── dataset_creation_single.ipynb
```

This repository is split into three sections:

- **Synthetic data creation** (see `synthetic_data_creation`): Notebooks required to create the synthetic datasets from the real ABFE data
- **Computation of equilibration times** (see `compute_equil_times`): Scripts to calculate the equilibration times for the synthetic dataset using [`RED`](https://github.com/fjclark/red)
- **Analysis** (see `analysis`): Notebooks to analyse the performance of the equilibration detection methods

For all notebooks, `_free` denotes the free vanish multi-window data and `_single` denotes the bound vanish single-window data - otherwise the notebooks deal with the standard bound vanish multi-window data.

To rerun any of the steps, create the environment with
```bash
make env
mamba activate red_reproduce
```
and rerun the desired notebooks/ scripts.
