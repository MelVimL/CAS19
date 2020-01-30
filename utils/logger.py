import logging

DEFAULT_LOG_LEVEL   = "ERROR"
DEFAULT_LOG_FORMAT  = "%(asctime)s %(levelname)s (%(threadName)s): %(message)s"


def setup_logger(config):
    handlers = []
    if config.get("console_active", True):
        handlers.append(logging.StreamHandler())
    if config.get("file_active", True):
        handlers.append(logging.FileHandler(config.get("file_path", "./log/default.log")))
    level = config.get("level", DEFAULT_LOG_LEVEL)
    format = config.get("format", DEFAULT_LOG_FORMAT)
    logging.basicConfig(level=level, format=format, handlers=handlers)