# benchmark/benchmark.py
import time
from src.main import RedisPlus

def run_benchmarks(redis: RedisPlus, num_operations: int = 10000):
    start_time = time.time()
    for i in range(num_operations):
        redis.set(f"key_{i}", f"value_{i}")
    set_time = time.time() - start_time

    start_time = time.time()
    for i in range(num_operations):
        redis.get(f"key_{i}")
    get_time = time.time() - start_time

    print(f"Set operations: {num_operations / set_time:.2f} ops/sec")
    print(f"Get operations: {num_operations / get_time:.2f} ops/sec")
    print("\nDetailed stats:")
    print(redis.get_stats())

if __name__ == '__main__':
    redis = RedisPlus()
    run_benchmarks(redis)