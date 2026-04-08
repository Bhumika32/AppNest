# backend/app/core/cache_service.py
import json
import logging
from typing import Optional, Any, Type, TypeVar

from app.core.redis_client import neural_cache

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CacheService:
    """
    Production-safe cache layer

    - JSON safe serialization
    - Type-aware loading
    - Namespaced keys
    - Failure-safe (never crash app)
    """

    PREFIX = "appnest"

    # -----------------------------
    # KEY BUILDER (MANDATORY)
    # -----------------------------
    @staticmethod
    def build_key(*parts: str) -> str:
        return f"{CacheService.PREFIX}:" + ":".join(parts)

    # -----------------------------
    # GET JSON (RESTORED ✅)
    # -----------------------------
    @staticmethod
    def get_json(key: str) -> Optional[Any]:
        try:
            cached = neural_cache.get(key)

            if not cached:
                return None

            if isinstance(cached, bytes):
                cached = cached.decode("utf-8")

            return json.loads(cached)

        except json.JSONDecodeError:
            logger.error(f"[CACHE CORRUPTION] key={key}")
            neural_cache.delete(key)
            return None

        except Exception as e:
            logger.warning(f"[CACHE GET FAILED] key={key} error={e}")
            return None

    # -----------------------------
    # GET WITH TYPE VALIDATION
    # -----------------------------
    @staticmethod
    def get_typed(key: str, expected_type: Type[T]) -> Optional[T]:
        data = CacheService.get_json(key)

        if data is None:
            return None

        if not isinstance(data, expected_type):
            logger.warning(f"[CACHE TYPE MISMATCH] key={key}")
            neural_cache.delete(key)
            return None

        return data

    # -----------------------------
    # SET JSON (FIXED ✅ no duplicate)
    # -----------------------------
    @staticmethod
    def set_json(
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        ex: Optional[int] = None,
    ) -> bool:
        """
        Set JSON value in cache

        Supports:
        - ttl (preferred)
        - ex (Redis native)
        """

        try:
            serialized = json.dumps(value, default=str)

            expire = ttl if ttl is not None else ex

            if expire:
                return neural_cache.set(key, serialized, ex=expire)

            return neural_cache.set(key, serialized)

        except Exception as e:
            logger.warning(f"[CACHE SET FAILED] key={key} error={e}")
            return False

    # -----------------------------
    # DELETE
    # -----------------------------
    @staticmethod
    def delete(key: str) -> bool:
        try:
            neural_cache.delete(key)
            return True
        except Exception as e:
            logger.warning(f"[CACHE DELETE FAILED] key={key} error={e}")
            return False

    # -----------------------------
    # BULK INVALIDATION (SCAN SAFE)
    # -----------------------------
    @staticmethod
    def delete_pattern(pattern: str):
        try:
            cursor = 0
            while True:
                cursor, keys = neural_cache.scan(
                    cursor=cursor, match=pattern, count=100
                )
                if keys:
                    neural_cache.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            logger.warning(f"[CACHE PATTERN DELETE FAILED] {pattern} error={e}")
