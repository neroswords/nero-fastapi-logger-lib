from fastapi_logger.default_logger import logger, generate_api_request_id, get_request_id

def test_logging():
    generate_api_request_id()
    request_id = get_request_id()
    logger.info(f"Test log with request_id: {request_id}")

if __name__ == "__main__":
    test_logging()
