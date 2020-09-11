import time

from src.app import get_logger

logger = get_logger(__name__)


class CacheMemoryService:
    def __init__(self):
        logger.info("INIT")
        self._values = {}

    def set_value(self, key: str,
                  value: object, ttl_in_seconds: int = 0) -> bool:
        if ttl_in_seconds < 0:
            return False
        self._values[key] = (
            value,
            0 if not ttl_in_seconds else time.time() + ttl_in_seconds,
        )
        return True

    def get_value(self, key: str) -> object:
        value = self._values.get(key, None)
        if value and (value[1] == 0 or value[1] >= time.time()):
            return value[0]
        self._values.pop(key, None)
