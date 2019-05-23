import glob
import os

PATTERNS = ("*.jpg", "*.png", "*.jpeg")
BASE_DIR = "/Users/krishna.tripathi/Documents/projects/hack_day/img_reco/hackday_9/img_files"


def get_full_path(files : list) -> list:
    files_grabbed = []
    print(files)
    for f in files:
        files_grabbed.extend(glob.glob(os.path.join(BASE_DIR, f)))
    return files_grabbed


def get_files(directory: list) -> list:
    files_grabbed = []
    for pattern in PATTERNS:
        files_grabbed.extend(glob.glob( os.path.join(BASE_DIR, directory, pattern)))

    print(files_grabbed)
    return files_grabbed
