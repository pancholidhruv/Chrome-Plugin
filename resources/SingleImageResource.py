from models.ImageMatch import ImageMatch
import os

PATTERNS = ("*.jpg", "*.png", "*.jpeg")


def get_score(path: str) -> ImageMatch:
    return ImageMatch(os.path.basename(path), "", "", {})


