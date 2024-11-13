# redis_data_structures.py
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from time import time

@dataclass
class RedisValue:
    value: Any
    expiry: Optional[float] = None

    def is_expired(self) -> bool:
        return self.expiry is not None and time() > self.expiry

class RedisString:
    def __init__(self):
        self.data: Dict[str, RedisValue] = {}

    def set(self, key: str, value: str, ex: Optional[int] = None):
        expiry = time() + ex if ex is not None else None
        self.data[key] = RedisValue(value, expiry)

    def get(self, key: str) -> Optional[str]:
        if key in self.data:
            value = self.data[key]
            if not value.is_expired():
                return value.value
            del self.data[key]
        return None

class RedisList:
    def __init__(self):
        self.data: Dict[str, List[Any]] = {}

    def lpush(self, key: str, value: Any):
        if key not in self.data:
            self.data[key] = []
        self.data[key].insert(0, value)

    def rpush(self, key: str, value: Any):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def lpop(self, key: str) -> Optional[Any]:
        if key in self.data and self.data[key]:
            return self.data[key].pop(0)
        return None