import os
import asyncio
from fastapi import FastAPI, Response, Request
from strictaccess import strict_access_control, private, public
from strictaccess import AccessControlMixin
import httpx
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .monitoring import REQUEST_COUNT, REQUEST_LATENCY
from .security import security
from .router import Router
from .config import config
from .registry import register_service  # 👈 usamos nuestro registry
import time

DISCOVERY_URL = os.getenv("DISCOVERY_URL", "http://localhost:8500")

@strict_access_control()
class Service:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.config = config
        self.app = FastAPI(title=f"Microstorm - {self.name}")
        self.client = httpx.AsyncClient()
        self.router = Router(self)

        @self.app.on_event("startup")
        async def startup_event():
            asyncio.create_task(self._auto_register())

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "service": self.name}

        @self.app.get("/metrics")
        async def metrics():
            data = generate_latest()
            return Response(content=data, media_type=CONTENT_TYPE_LATEST)

        @self.app.middleware("http")
        async def auth_middleware(request: Request, call_next):
            await security.verify_request(request)
            response = await call_next(request)
            return response

        @self.app.middleware("http")
        async def add_metrics(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time

            endpoint = request.url.path
            method = request.method

            REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)

            return response
        
        @private
        async def _auto_register(self):
            """Auto-registra el servicio en Discovery cada 20 segundos"""
            while True:
                try:
                    url = f"{DISCOVERY_URL}/register"
                    payload = {
                        "name": self.name,
                        "port": self.port,
                        "ttl": 30  # segundos
                    }
                    response = await self.client.post(url, json=payload)
                    if response.status_code == 200:
                        print(f"[Discovery] Re-registered {self.name} successfully.")
                    else:
                        print(f"[Discovery] Failed to register {self.name}: {response.status_code}")

                except Exception as e:
                    print(f"[Discovery] Error while registering: {e}")

                await asyncio.sleep(20)  # Reintenta cada 20 segundos


    def route(self, path: str, methods=["GET"]):
        def decorator(func):
            self.app.add_api_route(path, func, methods=methods)
            return func
        return decorator

    @public
    async def call_service(self, service_name: str, endpoint: str, method="GET", data=None, **kwargs):
        url = f"http://localhost:{self._service_port(service_name)}{endpoint}"
        attempt = 0
        backoff = self.config.retry_backoff

        while attempt <= self.config.max_retries:
            try:
                headers = {}
                security.attach_auth_header(headers)

                response = await self.client.request(
                    method, url, headers=headers, params=kwargs, json=data
                )
                response.raise_for_status()
                return response.json()

            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                print(f"[Warning] call_service attempt {attempt + 1} failed: {e}")

                if attempt == self.config.max_retries:
                    print(f"[Error] Max retries exceeded for {service_name} at {endpoint}")
                    return None

                await asyncio.sleep(backoff)
                backoff *= 2
                attempt += 1

            except Exception as e:
                print(f"[Error] call_service unexpected error: {e}")
                return None

    @private
    async def _auto_register(self):
        attempt = 0
        backoff = self.config.retry_backoff

        while attempt <= self.config.max_retries:
            try:
                register_service(self.name, self.port)
                print(f"[Service] Successfully auto-registered {self.name}")
                return  # Listo, terminamos

            except Exception as e:
                print(f"[Warning] Auto-register attempt {attempt + 1} failed: {e}")

                if attempt == self.config.max_retries:
                    print(f"[Error] Max retries exceeded during auto-registration.")
                    return

                await asyncio.sleep(backoff)
                backoff *= 2
                attempt += 1

    @public
    def run(self):
        # 👇 Hacemos auto-registro antes de arrancar el servidor
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._auto_register())

        # 👇 Luego lanzamos FastAPI normalmente
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)
