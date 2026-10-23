# Starter kit commands. Each one runs inside the uv environment. Run `just` to list them.
#   just setup                                   create the environment (.venv) with uv
#   just data                                    download and unpack the competition data into data/
#   just train                                   train the baseline, write submissions/baseline.csv
#   just check submissions/baseline.csv          validate a submission file
#   just submit submissions/baseline.csv "msg"   check, then upload
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

[private]
default:
    @just --list --unsorted

# create the environment (.venv) with uv
setup:
    uv sync

# download and unpack the competition data into data/
data:
    uv run python -m kit.download_data

# train the baseline, write submissions/baseline.csv
train:
    uv run python -m kit.train

# validate a submission file
check f="submissions/baseline.csv":
    uv run python -m kit.check_submission {{f}}

# check, then upload
submit f="submissions/baseline.csv" m="baseline":
    uv run python -m kit.submit {{f}} "{{m}}"
