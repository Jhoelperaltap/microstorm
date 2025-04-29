from prometheus_client import Counter, Histogram

# Contador de peticiones por método y endpoint
REQUEST_COUNT = Counter(
    'microstorm_request_count',
    'Total HTTP requests',
    ['method', 'endpoint']
)

# Histograma de duración de peticiones
REQUEST_LATENCY = Histogram(
    'microstorm_request_latency_seconds',
    'Latency of HTTP requests',
    ['endpoint']
)