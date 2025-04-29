import pytest
from microstorm.registry import Registry

@pytest.mark.asyncio
async def test_local_register_and_get():
    registry = Registry()
    registry._debug_mode = True
    registry.discovery_url = None  # Forzar uso local

    service_name = "test-service"
    port = 12345

    # No uses await si discovery_url es None
    registry.register_service(service_name, port)

    result = registry.get_service_port(service_name)
    assert result == port


registry = Registry()
registry._debug_mode = True
