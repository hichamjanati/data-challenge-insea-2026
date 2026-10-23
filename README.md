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

Each team member needs a Kaggle account. Log the command line in, once:

```sh
uv run kaggle auth login            # opens a browser, recommended
```

And login on the browser. Your credential token will automatically be saved in your home folder ~/.kaggle: keep it private from both humans (and agents !). 

## 4. Join the competition

1. Open the **competition invitation link** shared by the host, while logged in to your Kaggle account.
2. Click **Join Competition** and **accept the rules**. Without this, every download and submission is refused.
3. Form your team on Kaggle: one member opens the **Team** tab of the competition and invites the others.

The rules on the competition page are the ones that apply.

## 5. From data to submission

Run `just` alone to list the commands. Each one is a single line in `justfile`.

### Step 1: get the data

```sh
just data
```

Downloads and unpacks the tables and the photos into `data/` (about 400 MB, gitignored). Run it once.

### Step 2: train a model, in the notebook or with the scripts

**In the notebook.** Start Jupyter and open `notebooks/kaggle_starter.ipynb`:

```sh
uv run jupyter lab
```

Run all the cells: the notebook trains the baseline and writes `submissions/submission.csv`.

**With the scripts.** Run the baseline:

```sh
just train
```

This runs `kit/train.py`: it trains the baseline, prints its cross-validated log loss and writes the predictions for the
test ads to `submissions/baseline.csv`. Edit `kit/train.py` (or write your own script) to improve it.

### Step 3: check the submission file

```sh
just check submissions/baseline.csv
```

Validates the file the way Kaggle does, and warns about predictions that will cost you. Use the path of your own file,
for example `submissions/submission.csv` if it comes from the notebook.

### Step 4: submit

```sh
just submit submissions/baseline.csv "baseline: LDA on the table"
```

Checks the file again, asks for confirmation, then uploads it with your message. **Careful: you have one submission
per day per team**, so make sure the file is the one you want before typing `y`. On Windows, keep `$` out of the message:
PowerShell would replace it.

Submission files are gitignored: keep the code that produced them instead.

## 6. What is in the kit


| file                             | role                                                                                    |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| `kit/data.py`                    | paths, the competition name, loaders for the tables and for the photos of one ad        |
| `kit/download_data.py`           | `just data`                                                                             |
| `kit/train.py`                   | the baseline: LDA with default settings on the table columns, complete rows only        |
| `kit/check_submission.py`        | the format checks Kaggle applies, plus warnings on predictions that will cost you       |
| `kit/submit.py`                  | `just submit`                                                                           |
| `notebooks/kaggle_starter.ipynb` | the same baseline as a notebook, runs unchanged on your laptop or on Kaggle (section 7) |
| `REPORT.md`                      | the report skeleton to fill in for the oral evaluation                                  |


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