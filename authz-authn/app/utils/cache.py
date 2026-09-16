import json
import os
from typing import Any

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)


class CacheManager:
    def __init__(
        self,
        host: str = REDIS_HOST,
        port: int = REDIS_PORT,
        password: str | None = REDIS_PASSWORD,
    ):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
        )

    def ping(self) -> bool:
        try:
            return self.redis_client.ping()
        except redis.RedisError as error:
            print(f"Redis connection check failed: {error}")
            return False

    def store_data(self, key: str, value: Any, time_to_live: int | None = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            if time_to_live is None:
                self.redis_client.set(key, value)
            else:
                self.redis_client.setex(key, time_to_live, value)
            return True
        except redis.RedisError as error:
            print(f"An error occurred while storing data in Redis: {error}")
            return False

    def get_data(self, key: str) -> str | None:
        try:
            return self.redis_client.get(key)
        except redis.RedisError as error:
            print(f"An error occurred while retrieving data from Redis: {error}")
            return None

    def check_key(self, key: str) -> tuple[bool, int | None]:
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                ttl = self.redis_client.ttl(key)
                return True, ttl if ttl >= 0 else None
            return False, None
        except redis.RedisError as error:
            print(f"An error occurred while checking a key in Redis: {error}")
            return False, None

    def delete_data(self, key: str) -> bool:
        try:
            return self.redis_client.delete(key) > 0
        except redis.RedisError as error:
            print(f"An error occurred while deleting data from Redis: {error}")
            return False

    def delete_data_with_pattern(self, pattern: str) -> int:
        try:
            deleted_count = 0
            batch = []
            for key in self.redis_client.scan_iter(match=pattern, count=100):
                batch.append(key)
                if len(batch) >= 100:
                    deleted_count += self.redis_client.delete(*batch)
                    batch.clear()

            if batch:
                deleted_count += self.redis_client.delete(*batch)

            return deleted_count
        except redis.RedisError as error:
            print(f"An error occurred while bulk deleting keys: {error}")
            return 0
