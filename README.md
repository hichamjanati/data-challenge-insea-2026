# INSEA 2026 data challenge: starter kit

Will this used car sell within 30 days? Each ad has a table row, a title and description in French, and up to 4 photos.
You predict a probability for each test ad; submissions are scored with the log loss.
Competition page, data description and rules: [https://www.kaggle.com/competitions/multimodal-predictive-ml-data-challenge](https://www.kaggle.com/competitions/multimodal-predictive-ml-data-challenge)

This repository is a starting point: an environment, the data download, a weak baseline, a submission checker and
the upload command. Everything in it is meant to be replaced by your own work.

## 1. Create your team repository

1. Click **Use this template** (top right), then **Create a new repository**. Make it **private** and give it your team's name.
  Do not fork: a fork of a public repository cannot be private.
2. In your repository, **Settings > Collaborators**, add the instructor.
3. Clone your repository and work in it. Everything below runs from its root folder.



## 2. Environment

The kit uses [uv](https://docs.astral.sh/uv/) for the environment and [just](https://just.systems/) to run its commands. Follow the instructions for your system.

### Windows

Open **PowerShell** (Start menu, type "PowerShell"). Install uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell, open a new one, go to your repository folder, then install just and create the environment:

```powershell
uv tool install rust-just
just setup
```

If PowerShell says `just` is not recognized, run `uv tool update-shell`, then close and reopen PowerShell.

### macOS

Open **Terminal** (Applications > Utilities). Install uv:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal, open a new one, go to your repository folder, then install just and create the environment:

```sh
uv tool install rust-just
just setup
```

If the terminal says `just: command not found`, run `uv tool update-shell`, then close and reopen the terminal.

### Linux

Open a terminal. Install uv (if `curl` is missing, use `wget -qO- https://astral.sh/uv/install.sh | sh`):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal, open a new one, go to your repository folder, then install just and create the environment:

```sh
uv tool install rust-just
just setup
```

If the terminal says `just: command not found`, run `uv tool update-shell`, then close and reopen the terminal.

### On all systems

`just setup` creates `.venv` with numpy, pandas, scikit-learn, xgboost, lightgbm, matplotlib, pillow, kaggle and
jupyterlab. From here on, every command in this README is the same on Windows, macOS and Linux.

Add packages with `uv add <package>` (for example `uv add torch`); `pyproject.toml` records them, so the instructor can
rebuild your environment with `uv sync`. Run anything with `uv run python ...` or `uv run jupyter lab`.

## 3. Kaggle access

Each team member needs a Kaggle account that has **joined the competition** (open the competition link and accept the rules).
Then log the command line in, once:

```sh
uv run kaggle auth login            # opens a browser, recommended
```

And login on the browser. Your credential token will automatically be saved in your home folder ~/.kaggle: keep it private from both humans (and agents !). 

## 4. The four commands

```sh
just data                                   # downloads and unpacks everything into data/ (about 400 MB, gitignored)
just train                                  # trains the baseline, writes submissions/baseline.csv
just check submissions/baseline.csv         # validates a submission file
just submit submissions/baseline.csv "baseline: LDA on the table"   # checks, asks, uploads
```

Run `just` alone to list the commands. Each one is a single line in `justfile`; without just, run it directly:


| just                         | without just                                 |
| ---------------------------- | -------------------------------------------- |
| `just setup`                 | `uv sync`                                    |
| `just data`                  | `uv run python -m kit.download_data`         |
| `just train`                 | `uv run python -m kit.train`                 |
| `just check FILE`            | `uv run python -m kit.check_submission FILE` |
| `just submit FILE "MESSAGE"` | `uv run python -m kit.submit FILE "MESSAGE"` |


You have **one submission per day per team**: `just submit` asks for confirmation. Submission files are gitignored;
keep the code that produced them instead. On Windows, keep `$` out of the submission message: PowerShell would replace it.

## 5. What is in the kit


| file                             | role                                                                                    |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| `kit/data.py`                    | paths, the competition name, loaders for the tables and for the photos of one ad        |
| `kit/download_data.py`           | `just data`                                                                             |
| `kit/train.py`                   | the baseline: LDA with default settings on the table columns, complete rows only        |
| `kit/check_submission.py`        | the format checks Kaggle applies, plus warnings on predictions that will cost you       |
| `kit/submit.py`                  | `just submit`                                                                           |
| `notebooks/kaggle_starter.ipynb` | the same baseline as a notebook, runs unchanged on your laptop or on Kaggle (section 7) |
| `REPORT.md`                      | the report skeleton to fill in for the oral evaluation                                  |


The baseline ignores the text, the photos and part of the table, drops every training ad with a missing value, and gives
the train sale rate to every test ad with a missing value. Each of these choices is a place to start.

## 6. Rules in short

Teams of 2 or 3, one Kaggle team per student team, one submission per day, one final submission selected before the
deadline. Public pretrained models are allowed; external data is not. Your code must reproduce your final submission.
The full rules are on the competition page and are the ones that apply.

## 7. Working on Kaggle with a GPU

Kaggle notebooks give you a free GPU (a weekly quota of about 30 hours, shown in the notebook sidebar) and the
competition data already mounted, with no download.

1. On the competition page, open **Code**, find the starter notebook and click **Copy & Edit**.
2. In the notebook, **Settings > Accelerator** to pick a GPU, and **Internet: on** if you download a pretrained model
  (Kaggle asks for a phone verification the first time you enable either).
3. The data is at `/kaggle/input/multimodal-predictive-ml-data-challenge/`; write your submission to `/kaggle/working/submission.csv`.
4. **Save Version**, then in the saved version open **Output** and click **Submit to competition**. No file to download.

Keep the notebook's code in your team repository too (download it with **File > Download notebook**): the repository
is what must reproduce your final submission.