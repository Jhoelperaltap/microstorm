
import os
from strictaccess import strict_access_control, private, public
from strictaccess import AccessControlMixin

@strict_access_control()
class Config:
    def __init__(self):
        # Service settings
        self.service_name = os.getenv("SERVICE_NAME", "default-service")
        self.service_port = int(os.getenv("SERVICE_PORT", 8000))

        # Retry settings
        self.max_retries = int(os.getenv("MAX_RETRIES", 3))
        self.retry_backoff = float(os.getenv("RETRY_BACKOFF", 0.5))

        # Registry settings
        self.registry_file = os.getenv("REGISTRY_FILE", "services.json")

        # Security settings
        self.auth_secret_key = os.getenv("AUTH_SECRET_KEY", "mysecretkey")
        self.auth_algorithm = os.getenv("AUTH_ALGORITHM", "HS256")

        # Discovery settings (¡esto es lo nuevo!)
        self.discovery_url = os.getenv("DISCOVERY_URL", "http://localhost:8500")

        # Other future configs can go here...
    
    @public
    def display(self):
        print(f"[Config] Loaded configuration:")
        for attr in dir(self):
            if not attr.startswith("_") and not callable(getattr(self, attr)):
                print(f"    {attr}: {getattr(self, attr)}")

# Singleton instance
config = Config()
