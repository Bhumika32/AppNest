import redis
import json
import logging
from app.core.config import Config

logger = logging.getLogger(__name__)

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._fallback_cache = {}
            try:
                cls._instance.client = redis.from_url(
                    Config.REDIS_URL,
                    decode_responses=True
                )
                logger.info("Connected to Neural Cache (Redis)")
            except Exception as e:
                logger.warning(f"Redis unavailable, falling back to in-memory cache: {e}")
                cls._instance.client = None
        return cls._instance

    def get(self, key):
        if not self.client:
            return self._fallback_cache.get(key)
        try:
            val = self.client.get(key)
            return json.loads(val) if val else None
        except Exception as e:
            logger.warning(f"Redis get failed for {key}, using fallback: {e}")
            return self._fallback_cache.get(key)

    def set(self, key, value, ex=None):
        if not self.client:
            self._fallback_cache[key] = value
            return
        try:
            self.client.set(key, json.dumps(value), ex=ex)
            # Also update local cache for consistency during fallback transitions
            self._fallback_cache[key] = value
        except Exception as e:
            logger.error(f"Redis set failed for {key}, updating fallback: {e}")
            self._fallback_cache[key] = value

neural_cache = RedisClient()
