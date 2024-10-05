PACKAGE_NAME  := red_reproduce
CONDA_ENV_RUN := conda run --no-capture-output --name $(PACKAGE_NAME)

CREATION_NBS := $(shell find synthetic_data_creation -name 'dataset_creation*.ipynb')
ANALYSIS_NBS := $(shell find analysis -name 'analysis*.ipynb')
OUTPUT_DIRS := $(shell find synthetic_data_creation compute_equil_times analysis -type d -name 'output*')

.PHONY: all env download_data create_synthetic_data compute_equil_times analyse analyse_fast clean

# Default target. Clean is run after downloading all data to keep only the gradient arrays data (all
# other data is reproduced).
all: env download_data clean create_synthetic_data compute_equil_times analyse

env:
	mamba create     --name $(PACKAGE_NAME)
	mamba env update --name $(PACKAGE_NAME) --file devtools/envs/base.yaml
	$(CONDA_ENV_RUN) pip install --no-build-isolation --no-deps git+https://github.com/fjclark/red.git

download_data:
	# For the moment, just copy from outside the repo
	# Touch everything to update the timestamps
	touch -c ../robust_equil_detection_zenodo/*
	rsync -a ../robust_equil_detection_zenodo/ .

create_synthetic_data:
	$(CONDA_ENV_RUN) jupyter nbconvert --to notebook --execute $(CREATION_NBS)

compute_equil_times:
	$(CONDA_ENV_RUN) bash compute_equil_times/compute_equil_times.sh

analyse:
	$(CONDA_ENV_RUN) jupyter nbconvert --to notebook --execute $(ANALYSIS_NBS)

figures_only:
	FIGURES_ONLY=1 $(CONDA_ENV_RUN) jupyter nbconvert --to notebook --execute $(CREATION_NBS)
	FIGURES_ONLY=1 $(CONDA_ENV_RUN) jupyter nbconvert --to notebook --execute $(ANALYSIS_NBS)

# Note that clean does not remove the "gradient_arrays_30ns" data, because this is never
# modified - it's the starting point for the synthetic data creation.
clean:
	# Delete everything in the output directories
	find $(OUTPUT_DIRS) -mindepth 1 -delete
	# Clean all the notebooks
	nb-clean clean $(ANALYSIS_NBS) $(CREATION_NBS)
	# Remove any .nbconvert.ipynb notebooks
	find analysis synthetic_data_creation -name '*.nbconvert.ipynb' -type f -delete
