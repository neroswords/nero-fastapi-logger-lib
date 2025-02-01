from setuptools import setup, find_packages

setup(
    name="nero-fastapi-logger-lib",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "colorlog",
        "python-json-logger",
        "contextvars",
    ],
    author="Tanathap Roongpipat",
    author_email="tanathep.min@gmail.com",
    description="A logging library for FastAPI with request_id tracking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/neroswords/nero-fastapi-logger-lib.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
