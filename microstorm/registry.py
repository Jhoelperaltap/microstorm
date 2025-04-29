import os
import json
import threading
import httpx
from strictaccess import strict_access_control, private, public
from strictaccess import AccessControlMixin
from .config import config

_registry_lock = threading.Lock()

@strict_access_control()
class Registry:
    def __init__(self):
        self.discovery_url = config.discovery_url
        self.registry_file = config.registry_file

    @private
    def _load_registry_file(self):
        if not os.path.exists(self.registry_file):
            return {}
        with open(self.registry_file, "r") as f:
            return json.load(f)

    @private
    def _save_registry_file(self, data):
        with open(self.registry_file, "w") as f:
            json.dump(data, f, indent=4)

    @public
    def register_service(self, name, port):
        """Registra el servicio en archivo local o Discovery Server"""
        if self.discovery_url:
            return self._register_to_discovery(name, port)
        else:
            return self._register_to_file(name, port)

    @private
    def _register_to_file(self, name, port):
        with _registry_lock:
            registry = self._load_registry_file()
            registry[name] = port
            self._save_registry_file(registry)
            print(f"[Registry] Registered service '{name}' on port {port} (local file)")

    @private
    async def _register_to_discovery(self, name, port):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.discovery_url}/register",
                    json={"name": name, "port": port, "ttl": 30}

                )
                response.raise_for_status()
                print(f"[Registry] Registered service '{name}' on discovery server")
            except Exception as e:
                raise RuntimeError(f"Failed to register service with discovery: {e}")

    @public
    def get_service_port(self, name):
        """Obtiene el puerto del servicio"""
        if self.discovery_url:
            return self._get_from_discovery(name)
        else:
            return self._get_from_file(name)

    @private
    def _get_from_file(self, name):
        registry = self._load_registry_file()
        port = registry.get(name)
        if port is None:
            raise ValueError(f"Service '{name}' not found in registry file.")
        return port

    @private
    async def _get_from_discovery(self, name):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.discovery_url}/services")
                response.raise_for_status()
                services = response.json()
                service = services.get(name)
                if not service:
                    raise ValueError(f"Service '{name}' not found in discovery server.")
                return service["port"]
            except Exception as e:
                raise RuntimeError(f"Failed to fetch service from discovery: {e}")


# Singleton
registry = Registry()

# Para usar de manera simple:
register_service = registry.register_service
get_service_port = registry.get_service_port
