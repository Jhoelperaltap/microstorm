from pydantic import BaseModel

class ServiceRegisterRequest(BaseModel):
    name: str
    port: int
    ttl: int  # segundos de vida (Time to Live)

class ServiceResponse(BaseModel):
    name: str
    port: int
    expiry: float  # timestamp de expiración



class ServiceRegistration(BaseModel):
    name: str
    port: int
    ttl: int = 30  # segundos, default

