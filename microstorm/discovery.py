# discovery.py

import json
import os
import httpx
from strictaccess import strict_access_control, private, public
from strictaccess import AccessControlMixin
from .config import config

@strict_access_control()
class DiscoveryClient:
    def __init__(self):
        self.registry_file = config.registry_file
        self.discovery_url = os.getenv("DISCOVERY_URL", "http://localhost:8500")  # URL del servidor de discovery (Consul/Eureka)

    @private
    def _load_registry(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, "r") as f:
                return json.load(f)
        return {}

    @private
    async def _fetch_service_from_discovery(self, service_name: str):
        """
        Hace un llamado HTTP para descubrir información sobre el servicio desde un servidor de discovery (ej. Consul/Eureka).
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.discovery_url}/v1/catalog/service/{service_name}")
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            print(f"[Error] Discovery request failed: {e}")
            return None

    @private
    async def _register_service_to_discovery(self, service_name: str, host: str, port: int):
        """
        Registra el servicio en el servidor de discovery (Consul/Eureka).
        """
        payload = {
            "ID": service_name,
            "Name": service_name,
            "Tags": ["microstorm"],
            "Address": host,
            "Port": port
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.discovery_url}/v1/agent/service/register", json=payload)
                response.raise_for_status()
                print(f"[Discovery] Registered service '{service_name}' at {host}:{port}")
        except httpx.RequestError as e:
            print(f"[Error] Failed to register service: {e}")

    @private
    async def _deregister_service_from_discovery(self, service_name: str):
        """
        Elimina el servicio del servidor de discovery cuando se detiene.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{self.discovery_url}/v1/agent/service/deregister/{service_name}")
                response.raise_for_status()
                print(f"[Discovery] Deregistered service '{service_name}'")
        except httpx.RequestError as e:
            print(f"[Error] Failed to deregister service: {e}")

    @public
    async def get_service_info(self, service_name: str):
        """
        Obtiene información del servicio. Primero verifica en el archivo `services.json`.
        Si no se encuentra, consulta el servidor de discovery dinámico.
        """
        registry = self._load_registry()
        if service_name in registry:
            return {"host": "localhost", "port": registry[service_name]}

        service_info = await self._fetch_service_from_discovery(service_name)
        if service_info:
            service = service_info[0]  # Tomamos el primer servicio disponible
            return {"host": service["ServiceAddress"], "port": service["ServicePort"]}
        else:
            raise ValueError(f"Service '{service_name}' not found in registry or discovery server.")

    @public
    async def get_service_url(self, service_name: str):
        """
        Retorna la URL completa del servicio.
        """
        info = await self.get_service_info(service_name)
        return f"http://{info['host']}:{info['port']}"

    @public
    async def register_service(self, service_name: str, host: str, port: int):
        """
        Registra un servicio en el servidor de discovery cuando se inicia.
        """
        await self._register_service_to_discovery(service_name, host, port)

    @public
    async def deregister_service(self, service_name: str):
        """
        Elimina el servicio del servidor de discovery cuando se detiene.
        """
        await self._deregister_service_from_discovery(service_name)
