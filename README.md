# FastAPI Logger Library

This is a reusable logging library for FastAPI applications with request_id tracking.

## Installation
```bash
pip install nero-fastapi-logger-lib
```

## Usage
```python
from fastapi_logger.logger import logger

logger.info("Hello from FastAPI!")
```

```python with sqlalchemy
from fastapi_logger.logger import logger, setup_sqlalchemy_logging
setup_sqlalchemy_logging()
logger.info("Hello from FastAPI!")
```

## Features
- Request ID tracking for API & Cron jobs
- JSON & color log formatting
- Compatible with FastAPI middleware
