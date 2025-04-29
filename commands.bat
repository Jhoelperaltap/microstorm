@echo off
SETLOCAL ENABLEEXTENSIONS

IF "%1"=="test" (
    echo Running tests with Discovery Server...
    python run_tests.py
    EXIT /B
)

IF "%1"=="lint" (
    echo Running lint check...
    ruff check microstorm strictaccess discovery
    EXIT /B
)

IF "%1"=="coverage" (
    echo Running coverage analysis...
    pytest --cov=microstorm --cov=strictaccess --cov-report=term --cov-report=html
    EXIT /B
)

IF "%1"=="publish" (
    echo Building and publishing package...
    python setup.py sdist bdist_wheel
    twine upload dist/*
    EXIT /B
)

echo Invalid command.
echo Usage:
echo     commands.bat test       - Run tests
echo     commands.bat lint       - Check code quality
echo     commands.bat coverage   - Run tests with coverage
echo     commands.bat publish    - Build and upload package
EXIT /B
