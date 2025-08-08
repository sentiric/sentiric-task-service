# app/core/logging.py

import logging
import sys
import structlog
from app.core.config import settings

_log_setup_done = False

def setup_logging():
    """
    Tüm servislerde kullanılacak standart loglama yapılandırması.
    Ortama göre (development/production) farklı formatlayıcılar kullanır.
    """
    global _log_setup_done
    if _log_setup_done:
        return

    log_level = settings.LOG_LEVEL.upper()
    env = settings.ENV.lower()
    
    # Celery'nin kendi log yapılandırmasını devralmasını engelle
    from celery.utils.log import get_task_logger
    get_task_logger(__name__).propagate = True
    
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if env == "development":
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else: # production veya diğer
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    _log_setup_done = True
    logger = structlog.get_logger(__name__)
    logger.info("Loglama başarıyla yapılandırıldı.", env=env, log_level=log_level)