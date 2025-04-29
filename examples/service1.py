import asyncio
from microstorm.service import Service
from microstorm.registry import register_service

service = Service(name="service1", port=9001)

@service.route("/hello", methods=["GET"])
async def hello():
    return {"message": "Hello from Service 1!"}

async def main():
    await register_service("service1", 9001)
    service.run()

if __name__ == "__main__":
    asyncio.run(main())
