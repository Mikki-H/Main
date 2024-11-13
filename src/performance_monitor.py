# performance_monitor.py
import time
from typing import Dict, List
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.operation_times: Dict[str, List[float]] = defaultdict(list)
        self.operation_counts: Dict[str, int] = defaultdict(int)

    def record_operation(self, operation: str, duration: float):
        self.operation_times[operation].append(duration)
        self.operation_counts[operation] += 1

    def get_average_time(self, operation: str) -> float:
        times = self.operation_times.get(operation, [])
        return sum(times) / len(times) if times else 0

    def get_operation_count(self, operation: str) -> int:
        return self.operation_counts.get(operation, 0)

class OperationTimer:
    def __init__(self, monitor: PerformanceMonitor, operation: str):
        self.monitor = monitor
        self.operation = operation
        self.start_time = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.monitor.record_operation(self.operation, duration)