import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    # Project settings
    PROJECT_NAME = "Test Automation Framework"
    VERSION = "1.0.0"
    
    # Timeouts
    DEFAULT_TIMEOUT = 30000  # 30 seconds
    EXPECT_TIMEOUT = 10000   # 10 seconds
    
    # Path settings
    DATA_DIR = BASE_DIR / "config"
    REPORTS_DIR = BASE_DIR / "reports"
    SCREENSHOTS_DIR = REPORTS_DIR / "reports/screenshots"
    LOGS_DIR = BASE_DIR / "logs"

    # Downloads directory
    DOWNLOADS_DIR = BASE_DIR / "downloads"

    @classmethod
    def get_log_file_path(cls):
        return cls.LOGS_DIR / "test_logs.log"


settings = Settings()
settings.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

