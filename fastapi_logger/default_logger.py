import logging
import logging.config
import uuid
import os
import contextvars
import colorlog
from pythonjsonlogger import jsonlogger

# Context variables for request_id
api_request_id_var = contextvars.ContextVar("api_request_id", default=None)
cronjob_request_id_var = contextvars.ContextVar("cronjob_request_id", default=None)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Generate & Retrieve Request ID
def generate_api_request_id():
    """Generate a unique request_id for API calls."""
    request_id = str(uuid.uuid4())
    api_request_id_var.set(request_id)
    return request_id

def generate_cronjob_request_id():
    """Generate a unique request_id for cron jobs."""
    request_id = str(uuid.uuid4())
    cronjob_request_id_var.set(request_id)
    return request_id

def get_request_id():
    """Get the request_id for API or CronJob execution."""
    return api_request_id_var.get() or cronjob_request_id_var.get() or generate_cronjob_request_id()

def clear_api_request_id():
    """Clear request_id after API response is sent."""
    api_request_id_var.set(None)

def clear_cronjob_request_id():
    """Clear request_id after cron job completes."""
    cronjob_request_id_var.set(None)

# Custom Logging Filter to Inject request_id
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id") or not record.request_id:
            record.request_id = get_request_id()
        return True

# Custom JSON Log Formatter
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = self.formatTime(record)
        log_record["level"] = record.levelname
        log_record["message"] = record.getMessage()
        log_record["request_id"] = getattr(record, "request_id", get_request_id())

# Custom Logger Adapter for SQLAlchemy
class RequestIDLoggerAdapter(logging.LoggerAdapter):
    """Ensures every log includes a consistent request_id within a cron job or API call."""

    def process(self, msg, kwargs):
        request_id = get_request_id()
        return f"[request_id={request_id}] {msg}", kwargs

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id_filter": {
            "()": RequestIDFilter,
        }
    },
    "formatters": {
        "json": {
            "()": CustomJsonFormatter,
            "format": "%(timestamp)s %(request_id)s %(level)s %(message)s",
        },
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "color",
            "filters": ["request_id_filter"],
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "logs/app.log",
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

# Apply Logging Configuration
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app_logger")
logger.addFilter(RequestIDFilter())

def setup_sqlalchemy_logging():
    """
    Enable SQLAlchemy logging with request_id tracking.
    Call this function if you want to track database queries.
    """
    sqlalchemy_loggers = ["sqlalchemy.engine", "sqlalchemy.pool"]
    
    for log_name in sqlalchemy_loggers:
        log = logging.getLogger(log_name)
        log.setLevel(logging.INFO)
        sqlalchemy_logger = RequestIDLoggerAdapter(log)

        # Apply adapter to all handlers
        for handler in log.handlers:
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.info("SQLAlchemy logging setup complete.")

logger.info("Logging setup complete.")
