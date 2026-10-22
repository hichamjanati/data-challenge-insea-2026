"""Check a submission file, then upload it to Kaggle.

Usage: uv run python -m kit.submit submissions/<file>.csv "a short message describing the model"
You have 1 submission per day: the script asks for confirmation before uploading.
"""
import subprocess, sys
from kit.check_submission import check
from kit.data import COMPETITION

if len(sys.argv) != 3:
    sys.exit(__doc__)
path, message = sys.argv[1], sys.argv[2]
check(path)
answer = input(f"upload {path} to {COMPETITION}? This uses today's submission [y/N] ")
if answer.strip().lower() != "y":
    sys.exit("not uploaded")
cmd = ["kaggle", "competitions", "submit", "-c", COMPETITION, "-f", path, "-m", message]
print(" ".join(cmd))
sys.exit(subprocess.run(cmd).returncode)
