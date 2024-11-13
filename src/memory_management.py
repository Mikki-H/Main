# memory_management.py
import struct
from typing import Optional

class Segment:
    SEGMENT_SIZE = 8 * 1024 * 1024  # 8MB

    def __init__(self):
        self.memory = bytearray(self.SEGMENT_SIZE)
        self.head = 0
        self.index = []

    def allocate(self, size: int) -> Optional[int]:
        if self.head + size > self.SEGMENT_SIZE:
            return None
        start = self.head
        self.head += size
        return start

    def store_object(self, key: str, value: str, expire: Optional[float] = None) -> Optional[int]:
        key_len = len(key)
        value_len = len(value)
        initial_size = 4 + 8 + 4 + key_len + value_len  # InitialSize + Expire + KeyLen + Key + Value
        start = self.allocate(initial_size)
        if start is None:
            return None
        struct.pack_into('I', self.memory, start, initial_size)
        struct.pack_into('d', self.memory, start + 4, expire if expire else 0)
        struct.pack_into('I', self.memory, start + 12, key_len)
        self.memory[start + 16:start + 16 + key_len] = key.encode()
        self.memory[start + 16 + key_len:start + 16 + key_len + value_len] = value.encode()
        self.index.append((key, start))
        return start

    def get_object(self, start: int) -> Optional[tuple]:
        initial_size = struct.unpack_from('I', self.memory, start)[0]
        expire = struct.unpack_from('d', self.memory, start + 4)[0]
        key_len = struct.unpack_from('I', self.memory, start + 12)[0]
        key = self.memory[start + 16:start + 16 + key_len].decode()
        value = self.memory[start + 16 + key_len:start + initial_size].decode()
        return (key, value, expire)

    def delete_object(self, start: int):
        struct.pack_into('I', self.memory, start, 0)  # Mark as deleted