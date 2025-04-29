import asyncio
from microstorm.service import Service
from microstorm.registry import register_service

service = Service(name="service2", port=9002)

@service.route("/proxy-hello", methods=["GET"])
async def proxy_hello():
    # Llama a service1 en su endpoint /hello
    response = await service.call_service("service1", "/hello")
    return {"proxied_response": response}

async def main():
    await register_service("service2", 9002)
    service.run()

if __name__ == "__main__":
    asyncio.run(main())
