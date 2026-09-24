import json
import os
from config.settings import settings

def load_test_data():
    """Loads test data from the configuration file."""
    data_file = os.path.join(settings.DATA_DIR, "test_data.json")
    with open(data_file, 'r') as f:
        return json.load(f)
