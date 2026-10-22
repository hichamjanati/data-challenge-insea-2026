# Starter kit: four commands. Each one runs inside the uv environment.
#   make setup     create the environment (.venv) with uv
#   make data      download and unpack the competition data into data/
#   make train     train the baseline, write submissions/baseline.csv
#   make check     validate a submission file:   make check F=submissions/baseline.csv
#   make submit    check, then upload:           make submit F=submissions/baseline.csv M="baseline"
F ?= submissions/baseline.csv
M ?= baseline

.PHONY: setup data train check submit

setup:
	uv sync

data:
	uv run python -m kit.download_data

train:
	uv run python -m kit.train

check:
	uv run python -m kit.check_submission $(F)

submit:
	uv run python -m kit.submit $(F) "$(M)"
