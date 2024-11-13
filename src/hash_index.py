# hash_index.py
import xxhash
from typing import Optional, Any

class TwoLevelHashIndex:
    def __init__(self):
        self.primary_index = {}
        self.secondary_index = {}

    def insert(self, key: str, value: Any):
        hash_value = xxhash.xxh64(key).intdigest()
        primary_key = hash_value >> 16
        secondary_key = hash_value & 0xFFFF

        if primary_key not in self.primary_index:
            self.primary_index[primary_key] = {}
        self.primary_index[primary_key][secondary_key] = value

    def get(self, key: str) -> Optional[Any]:
        hash_value = xxhash.xxh64(key).intdigest()
        primary_key = hash_value >> 16
        secondary_key = hash_value & 0xFFFF

        return self.primary_index.get(primary_key, {}).get(secondary_key)

    def delete(self, key: str):
        hash_value = xxhash.xxh64(key).intdigest()
        primary_key = hash_value >> 16
        secondary_key = hash_value & 0xFFFF

        if primary_key in self.primary_index and secondary_key in self.primary_index[primary_key]:
            del self.primary_index[primary_key][secondary_key]