"""Paths, competition constants and loaders shared by the scripts."""
from pathlib import Path
import pandas as pd
from PIL import Image

COMPETITION = "multimodal-predictive-ml-data-challenge"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
IMAGES = DATA / "images"
SUBMISSIONS = ROOT / "submissions"

TARGET = "sold_30d"
N_TEST = 19_919


def load_train() -> pd.DataFrame:
    return pd.read_csv(DATA / "train.csv")


def load_test() -> pd.DataFrame:
    return pd.read_csv(DATA / "test.csv")


def photo_names(row) -> list[str]:
    """The photo file names of one ad (an empty list when it has none)."""
    files = row["image_files"]
    return [] if pd.isna(files) or not files else files.split(";")


def load_photos(row) -> list[Image.Image]:
    """The photos of one ad as PIL images, 128 x 128 RGB."""
    return [Image.open(IMAGES / f).convert("RGB") for f in photo_names(row)]
