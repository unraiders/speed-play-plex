import random
import contextvars
import logging

from colorama import Fore, Style, init

from config import DEBUG

# Inicializar colorama
# Asegura que los códigos ANSI no se eliminen en macOS.
init(strip=False)

COLORS = {
    logging.DEBUG: Fore.GREEN,
    logging.INFO: Fore.WHITE,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}

trace_id_var = contextvars.ContextVar("trace_id")
class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get("----")
        return True
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Aplicar color según el nivel del log
        color = COLORS.get(record.levelno, Fore.WHITE)
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = ColoredFormatter("[%(asctime)s] [%(trace_id)s] [%(levelname)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
        handler.setFormatter(formatter)
        handler.addFilter(TraceIdFilter())
        logger.addHandler(handler)

    # Control exhaustivo de librerías de terceros
    third_party_loggers = [
        'qbittorrentapi',
        'urllib3',
        'requests',
        'urllib3.connectionpool',
        'qbittorrentapi.decorators'
    ]

    for lib in third_party_loggers:
        lib_logger = logging.getLogger(lib)
        lib_logger.setLevel(logging.WARNING)
        lib_logger.propagate = False
        for handler in lib_logger.handlers[:]:
            lib_logger.removeHandler(handler)

    return logger

def generate_trace_id():
    trace_id_var.set(random.randint(1000, 9999))

