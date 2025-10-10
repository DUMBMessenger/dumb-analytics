import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "analytics.db"
DB_AUTH_PATH = DATA_DIR / "authorization.db"
IS_SETUPED_PATH = DATA_DIR / "setup.lock"

os.makedirs(DATA_DIR, exist_ok=True)