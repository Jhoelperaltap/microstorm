from microstorm.service import Service

def test_service_initialization():
    svc = Service("test-service", 8000)
    assert svc.name == "test-service"
    assert svc.port == 8000
    assert svc.app is not None
    assert svc.router is not None