"""Download the competition data into data/ with the Kaggle API.

Needs a logged-in Kaggle CLI (uv run kaggle auth login) and the competition rules accepted on the website.
Usage: uv run python -m kit.download_data
"""
import shutil, subprocess, sys, zipfile
from kit.data import COMPETITION, DATA, IMAGES

CSVS = ["train.csv", "test.csv", "sample_submission.csv", "image_credits.csv"]

DATA.mkdir(exist_ok=True)
if (DATA / "train.csv").exists() and IMAGES.exists():
    print(f"data/ already populated ({DATA}); delete it to download again"); sys.exit(0)

cmd = ["kaggle", "competitions", "download", "-c", COMPETITION, "-p", str(DATA)]
print(" ".join(cmd))
r = subprocess.run(cmd)
if r.returncode != 0:
    # the full archive can be missing (404) while Kaggle builds it; the tables still come one file at a time
    print("full archive unavailable, downloading the tables one by one")
    for f in CSVS:
        r = subprocess.run(cmd + ["-f", f])
        if r.returncode != 0:
            sys.exit("download failed: are you logged in (uv run kaggle auth login), and did you accept the rules on the competition page?")
        if (DATA / f"{f}.zip").exists():
            with zipfile.ZipFile(DATA / f"{f}.zip") as zf:
                zf.extractall(DATA)
            (DATA / f"{f}.zip").unlink()
    sys.exit("tables downloaded, but not the photos: the full archive is not available yet. "
             "The baseline (just train) runs on the tables; run just data again later to get the photos.")

# the API delivers one archive with every competition file; the photos are a second archive inside it
for z in sorted(DATA.glob("*.zip")):
    if z.name == "images.zip":
        continue
    print(f"extracting {z.name}")
    with zipfile.ZipFile(z) as zf:
        zf.extractall(DATA)
    z.unlink()
if (DATA / "images.zip").exists() and not IMAGES.exists():
    print("extracting images.zip (98,119 photos, takes a minute)")
    with zipfile.ZipFile(DATA / "images.zip") as zf:
        zf.extractall(DATA)
    (DATA / "images.zip").unlink()
# Kaggle unpacks the uploaded images.zip server side, so the archive holds images/images/*.jpg
nested = IMAGES / "images"
if nested.is_dir():
    for p in nested.iterdir():
        p.rename(IMAGES / p.name)
    shutil.rmtree(nested)

missing = [f for f in CSVS if not (DATA / f).exists()]
n_img = len(list(IMAGES.glob("*.jpg"))) if IMAGES.exists() else 0
print(f"files: {', '.join(CSVS)}; photos: {n_img:,}")
if missing or n_img == 0:
    sys.exit(f"something is missing: {missing or 'photos'}; look at the content of data/")
print("done")
