from fastapi import FastAPI
from microstorm.router import Router

def test_router_initialization_and_routes():
    app = FastAPI()
    class DummyService:
        def __init__(self):
            self.app = app

    service = DummyService()
    router = Router(service)
    router._debug_mode = True  # activar debug para evitar restricciones

    @router.get("/test")
    async def test_endpoint():
        return {"ok": True}

    routes = [route.path for route in app.routes]
    assert "/test" in routes