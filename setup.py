from setuptools import setup, find_packages

setup(
    name="microstorm",
    version="0.1.2",
    author="Jhoel Peralta",
    author_email="jhoelperalta@gmail.com",
    description="A modern microservices toolkit for Python with built-in discovery, metrics, and security.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jhoelperaltap/microstorm",
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "httpx",
        "prometheus_client",
        "python-dotenv",
        "PyJWT",
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "ruff",
        "twine"
    ],
    classifiers = [
    "Programming Language :: Python :: 3",
    "Framework :: FastAPI",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
]
,
    python_requires='>=3.8',
)
