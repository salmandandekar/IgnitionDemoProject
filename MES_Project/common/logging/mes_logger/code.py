
import logging
from .log_factory import configure_root
def get_logger(name="MES"):
    configure_root(); return logging.getLogger(name)
