import logging
import sys
import json
import contextvars
from datetime import datetime

# Context variables (used per request)
request_id_var = contextvars.ContextVar("request_id", default=None)
user_var = contextvars.ContextVar("user", default=None)
path_var = contextvars.ContextVar("path", default=None)
method_var = contextvars.ContextVar("method", default=None)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Add request context automatically
        request_id = request_id_var.get()
        user = user_var.get()
        path = path_var.get()
        method = method_var.get()

        if request_id:
            log_record["request_id"] = request_id
        if user:
            log_record["user"] = user
        if path:
            log_record["path"] = path
        if method:
            log_record["method"] = method

        return json.dumps(log_record)


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )


def get_logger(name: str):
    return logging.getLogger(name)
