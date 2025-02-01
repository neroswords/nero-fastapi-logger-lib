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

want to setup with sqlalchemy logger
```python with sqlalchemy
from fastapi_logger.logger import logger, setup_sqlalchemy_logging
setup_sqlalchemy_logging()
logger.info("Hello from FastAPI!")
```
example dbConnector for this sqlalchemy log
```
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.configs.env import Env

class DBManager:
    _engine = create_engine(
                Env.DATABASE_URL,
                pool_size=10,
                max_overflow=0,
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True
            )
    _Session = sessionmaker(bind=_engine)

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise Exception("Engine not initialized. Call initialize() first.")
        return cls._engine

    @classmethod
    def get_session(cls):
        if cls._Session is None:
            raise Exception("Engine not initialized. Call initialize() first.")
        return cls._Session()

    @classmethod
    def execute_raw_sql(cls, query, params=None, result_model=None):
        if cls._engine is None:
            raise Exception("Engine not initialized. Call initialize() first.")
        with cls._engine.connect() as connection:
            result = connection.execute(text(query), params)
            if result_model:
                # Map the result to the data class
                mapped_result = [result_model(**row) for row in result.mappings()]
                return mapped_result
            return result.fetchall()

```

to setup with each request
```
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = generate_api_request_id()  # Set API request_id at start
        response = await call_next(request)
        response.headers['X-Request-ID'] = request_id
        clear_api_request_id()  # Clear API request_id after response
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the start of the request
        logger.info(f"Started {request.method} {request.url}")

        # Continue handling the request
        response = await call_next(request)

        # Log the end of the request
        logger.info(f"Completed {request.method} {request.url} with status code {response.status_code}")

        return response

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
```

## Features
- Request ID tracking for API & Cron jobs
- JSON & color log formatting
- Compatible with FastAPI middleware
