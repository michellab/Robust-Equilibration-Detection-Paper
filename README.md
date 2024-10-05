# Robust-Equilibration-Detection-Paper

**To reproduce the paper**:
```
git clone https://github.com/michellab/Robust-Equilibration-Detection-Paper.git
cd Robust-Equilibration-Detection-Paper
make all
```

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

To reproduce the paper, you will require `make` installed on your system. If you would like to play around with the data and analysis using the same synthetic data as in the paper, run:

```bash
make env
make download_data # Downloads the large files from Zenodo
make figures_only
```

This will pull all data from Zenodo and recreate all figures, without running computationally expensive steps. This will take a few minutes.

If you would like to reproduce the entire paper, including generation of the synthetic data and computation of equilibration times, run:

```bash
make all
```

Note that this is computationally expensive (due to the repeated calculation of equilibration times on thousands of synthetic datasets) and will take a few hours to complete.

You can clean any generated files with:

```bash
make clean
```