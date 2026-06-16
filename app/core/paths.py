from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

LOGS_DIR = PROJECT_ROOT / "logs"

API_LOGS_DIR = LOGS_DIR / "api"
SERVICE_LOGS_DIR = LOGS_DIR / "services"
REPOSITORY_LOGS_DIR = LOGS_DIR / "repositories"
SYSTEM_LOGS_DIR = LOGS_DIR / "system"


for directory in [
    LOGS_DIR,
    API_LOGS_DIR,
    SERVICE_LOGS_DIR,
    REPOSITORY_LOGS_DIR,
    SYSTEM_LOGS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
