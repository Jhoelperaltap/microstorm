import os
from strictaccess import strict_access_control, public
from fastapi import Request, HTTPException
from dotenv import load_dotenv
import jwt

load_dotenv()

@strict_access_control()
class Security:
    def __init__(self):
        self._service_token = os.getenv("SERVICE_TOKEN")
        self._secret_key = os.getenv("AUTH_SECRET_KEY", "mysecret")
        self._algorithm = os.getenv("AUTH_ALGORITHM", "HS256")

        if not self._service_token:
            raise RuntimeError("SERVICE_TOKEN environment variable not set.")

    @public
    def attach_auth_header(self, headers: dict):
        headers["Authorization"] = f"Bearer {self._service_token}"
        return headers

    @public
    async def verify_request(self, request: Request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

        token = auth.replace("Bearer ", "").strip()
        if token != self._service_token:
            raise HTTPException(status_code=403, detail="Invalid service token")

    @public
    def generate_token(self, payload: dict):
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    @public
    def verify_token(self, token: str):
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

# Singleton
security = Security()
