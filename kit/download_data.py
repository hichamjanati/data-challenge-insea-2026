"""Download the competition data into data/ with the Kaggle API.

Needs a logged-in Kaggle CLI (uv run kaggle auth login) and the competition rules accepted on the website.
Usage: uv run python -m kit.download_data
"""
import subprocess, sys, zipfile
from kit.data import COMPETITION, DATA, IMAGES

DATA.mkdir(exist_ok=True)
if (DATA / "train.csv").exists() and IMAGES.exists():
    print(f"data/ already populated ({DATA}); delete it to download again"); sys.exit(0)

cmd = ["kaggle", "competitions", "download", "-c", COMPETITION, "-p", str(DATA)]
print(" ".join(cmd))
r = subprocess.run(cmd)
if r.returncode != 0:
    sys.exit("download failed: are you logged in (uv run kaggle auth login), and did you accept the rules on the competition page?")

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

expected = ["train.csv", "test.csv", "sample_submission.csv", "image_credits.csv"]
missing = [f for f in expected if not (DATA / f).exists()]
n_img = len(list(IMAGES.glob("*.jpg"))) if IMAGES.exists() else 0
print(f"files: {', '.join(expected)}; photos: {n_img:,}")
if missing or n_img == 0:
    sys.exit(f"something is missing: {missing or 'photos'}; look at the content of data/")
print("done")
