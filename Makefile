PACKAGE_NAME  := red_reproduce
CONDA_ENV_RUN := conda run --no-capture-output --name $(PACKAGE_NAME)

.PHONY: env

env:
	mamba create     --name $(PACKAGE_NAME)
	mamba env update --name $(PACKAGE_NAME) --file devtools/envs/base.yaml
	$(CONDA_ENV_RUN) pip install --no-build-isolation --no-deps git+https://github.com/fjclark/red.git