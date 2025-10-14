import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "analytics.db"
DB_AUTH_PATH = DATA_DIR / "authorization.db"
IS_SETUPED_PATH = DATA_DIR / "setup.lock"

CERTS_DIR = BASE_DIR / "certs_api"
KEY_PEM = CERTS_DIR / "key.pem"
CERT_PEM = CERTS_DIR / "cert.pem"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)