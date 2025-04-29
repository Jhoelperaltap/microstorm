from fastapi import FastAPI
import uvicorn
import time
import asyncio
from .models import ServiceRegistration 

app = FastAPI(title="Microstorm Discovery Server 🚀")
registry = {}
DEFAULT_TTL = 30  # segundos

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time()}

@app.post("/register")
async def register_service(service: ServiceRegistration):
    expiry = time.time() + service.ttl
    registry[service.name] = {
        "port": service.port,
        "expiry": expiry,
        "ttl": service.ttl,
        "registered_at": time.time()
    }
    return {"message": f"Service {service.name} registered/updated with TTL {service.ttl} seconds."}

@app.get("/services")
async def list_services():
    now = time.time()
    active_services = {
        name: data for name, data in registry.items() if data["expiry"] > now
    }
    return active_services

async def cleanup_registry():
    while True:
        now = time.time()
        expired = [name for name, data in registry.items() if data["expiry"] < now]
        for name in expired:
            print(f"[Discovery] Removing expired service: {name}")
            del registry[name]
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_registry())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8500)
