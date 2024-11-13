# main.py
from src.memory_management import Segment
from .hash_index import TwoLevelHashIndex
from redis_data_structures import RedisString, RedisList
from performance_monitor import PerformanceMonitor, OperationTimer
from typing import Optional, Any, Dict

class RedisPlus:
    def __init__(self, memory_size: int = 1024 * 1024):
        self.memory = Segment()
        self.index = TwoLevelHashIndex()
        self.strings = RedisString()
        self.lists = RedisList()
        self.monitor = PerformanceMonitor()

    def set(self, key: str, value: str, ex: Optional[int] = None):
        with OperationTimer(self.monitor, 'set'):
            start = self.memory.store_object(key, value, ex)
            if start is not None:
                self.index.insert(key, start)

    def get(self, key: str) -> Optional[str]:
        with OperationTimer(self.monitor, 'get'):
            start = self.index.get(key)
            if start is not None:
                obj = self.memory.get_object(start)
                if obj and (obj[2] == 0 or obj[2] > time.time()):
                    return obj[1]
        return None
    def delete(self, key: str):
        with OperationTimer(self.monitor, 'delete'):
            start = self.index.get(key)
            if start is not None:
                self.memory.delete_object(start)
                self.index.delete(key)

    def lpush(self, key: str, value: Any):
        with OperationTimer(self.monitor, 'lpush'):
            self.lists.lpush(key, value)
            self.index.insert(f"list:{key}", value)

    def get_stats(self) -> Dict[str, Dict[str, float]]:
        return {
            'average_times': {
                op: self.monitor.get_average_time(op)
                for op in self.monitor.operation_times
            },
            'operation_counts': dict(self.monitor.operation_counts)
        }