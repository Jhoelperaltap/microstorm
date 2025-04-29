from microstorm.config import config

def test_config_defaults():
    # Activar modo debug para evitar errores de strictaccess
    config._debug_mode = True

    assert config.service_name == "default-service"
    assert isinstance(config.service_port, int)
    assert config.service_port == 8000

    assert isinstance(config.max_retries, int)
    assert config.max_retries == 3

    assert isinstance(config.retry_backoff, float)
    assert config.retry_backoff == 0.5

    assert config.registry_file == "services.json"
    assert config.auth_secret_key == "mysecretkey"
    assert config.auth_algorithm == "HS256"
    assert config.discovery_url.startswith("http")