import os

class Environment:
    """Handles environment-specific configurations."""
    
    ENV = os.getenv("TEST_ENV", "qa")
    
    _config = {
        "dev": {
            "base_url": "https://dev.example.com",
            "db_host": "dev-db.example.com",
        },
        "qa": {
            "base_url": "https://inmumvm26325635/wims",
            "db_host": "inmumvm26325635:3306"
        },
        "prod": {
            "base_url": "https://prod.example.com",
            "db_host": "prod-db.example.com",
        }
    }
    
    @classmethod
    def get_base_url(cls):
        return cls._config.get(cls.ENV, {}).get("base_url")

env = Environment()
