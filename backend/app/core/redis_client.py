"""app.core.redis_client
a Redis client wrapper that handles connection issues gracefully, with an in-memory fallback for development."""
import redis
import json
import logging
import time
from threading import Lock
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Production-ready Redis client with:
    - retry logic
    - reconnect handling
    - dev fallback
    """
    _instance = None
    _lock = Lock()

    MAX_RETRIES = 2 if settings.ENV == "development" else 5
    RETRY_DELAY = 0.5  # seconds

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client = None
        self.available = False
        self._fallback_cache = {}
        self._connect()

    def _connect(self):
        """Try connecting with retries"""
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                self.client = redis.from_url(
                    settings.REDIS_URL, decode_responses=True, socket_connect_timeout=settings.REDIS_CONNECT_TIMEOUT, socket_timeout=settings.REDIS_SOCKET_TIMEOUT, retry_on_timeout=True,
                )

                self.client.ping()

                self.available = True
                logger.info(f"✅ Redis connected (attempt {attempt})")
                return

            except Exception as e:
                logger.warning(f"Redis connection failed (attempt {attempt}): {e}")
                time.sleep(self.RETRY_DELAY)

        # After retries fail
        self.available = False
        self.client = None

        if settings.ENV == "production":
            logger.critical("❌ Redis unavailable after retries — crashing app")
            raise RuntimeError("Redis is required in production")
            

        logger.warning("⚠️ Falling back to in-memory cache (DEV ONLY)")

    def _ensure_connection(self):
        """Reconnect if Redis went down during runtime"""
        if not self.available:
            self._connect()

    def get(self, key):
        self._ensure_connection()
        if not self.available:
            return self._fallback_cache.get(key)

        try:
            val = self.client.get(key)
            return json.loads(val) if val else None

        except Exception as e:
            logger.error(f"Redis GET failed: {e}")
            self.available = False
            return self._fallback_cache.get(key)

    def set(self, key, value, ex=None, nx=False):
        if self.available:
            try:
                serialized = json.dumps(value)

                result = self.client.set(
                    key,
                    serialized,
                    ex=ex,
                    nx=nx
                )

                return bool(result)

            except Exception as e:
                logger.error(f"Redis SET failed: {e}")
                self.available = False
                return self.set(key, value, ex=ex, nx=nx)

        # fallback (DEV only)
        if nx and key in self._fallback_cache:
            return False
        
        self._fallback_cache[key] = {
            "value": value,
            "expires_at": time.time() + ex if ex else None
        }

    def delete(self, key):
        if self.available:
            try:
                self.client.delete(key)
                return True

            except Exception as e:
                logger.error(f"Redis DELETE failed: {e}")
                self.available = False
                return self.delete(key)

        self._fallback_cache.pop(key, None)
        return True

    def health(self):
        """Health check method"""
        try:
            if self.available:
                self.client.ping()
                return True
        except:
            self.available = False

        return False


neural_cache = RedisClient()
