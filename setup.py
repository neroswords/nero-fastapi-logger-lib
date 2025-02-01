from setuptools import setup, find_packages

setup(
    name="nero-fastapi-logger-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorlog",
        "python-json-logger",
    ],
    author="Tanathap Roongpipat",
    author_email="tanathep.min@gmail.com",
    description="A logging library for FastAPI with request_id tracking",
    url="https://github.com/neroswords/nero-fastapi-logger-lib.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
