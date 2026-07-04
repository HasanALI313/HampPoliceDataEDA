import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(os.getenv("POLICE_SOURCE_DIR", PROJECT_ROOT.parent / "source"))
OUTPUT_DIR = Path(os.getenv("POLICE_OUTPUT_DIR", PROJECT_ROOT / "output"))
BRONZE_DIR = OUTPUT_DIR / "bronze"
SILVER_DIR = OUTPUT_DIR / "silver"
GOLD_DIR = OUTPUT_DIR / "gold"
