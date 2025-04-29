import asyncio
import os
from microstorm.service import Service
from microstorm.registry import register_service
from microstorm.config import config

# Configuración explícita para usar Discovery Server
os.environ["DISCOVERY_URL"] = "http://localhost:8500"  # o usa .env
config.discovery_url = os.getenv("DISCOVERY_URL")      # Refresca si ya está importado

service = Service(name="service-discovery", port=9003)

@service.route("/info", methods=["GET"])
async def info():
    return {"message": "Usando Discovery Server", "discovery_url": config.discovery_url}

async def main():
    await register_service("service-discovery", 9003)
    service.run()

if __name__ == "__main__":
    asyncio.run(main())
