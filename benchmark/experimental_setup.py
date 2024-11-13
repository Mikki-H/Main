# experimental_setup.py
import random
import string
import time
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)  # Print the current sys.path

from src.main import RedisPlus

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_dataset(scale, key_size, value_size):
    dataset = []
    for _ in range(scale):
        key = generate_random_string(key_size)
        value = generate_random_string(value_size)
        dataset.append((key, value))
    return dataset

def test_memory_utilization(redis, dataset):
    for key, value in dataset:
        redis.set(key, value)
    print(f"Memory used: {redis.memory.head / (1024 * 1024)} MB")

def test_response_latency(redis, dataset):
    start_time = time.time()
    for key, value in dataset:
        redis.set(key, value)
    set_latency = (time.time() - start_time) / len(dataset)

    start_time = time.time()
    for key, _ in dataset:
        redis.get(key)
    get_latency = (time.time() - start_time) / len(dataset)

    print(f"Set latency: {set_latency * 1e6:.2f} µs")
    print(f"Get latency: {get_latency * 1e6:.2f} µs")

def test_throughput(redis, dataset):
    start_time = time.time()
    for key, value in dataset:
        redis.set(key, value)
    set_throughput = len(dataset) / (time.time() - start_time)

    start_time = time.time()
    for key, _ in dataset:
        redis.get(key)
    get_throughput = len(dataset) / (time.time() - start_time)

    print(f"Set throughput: {set_throughput:.2f} ops/sec")
    print(f"Get throughput: {get_throughput:.2f} ops/sec")

if __name__ == '__main__':
    redis = RedisPlus()
    tiny_dataset = create_dataset(10000, 8, 16)
    small_dataset = create_dataset(10000, 16, 128)
    large_dataset = create_dataset(10000, 128, 1024)

    print("Testing Tiny Dataset")
    test_memory_utilization(redis, tiny_dataset)
    test_response_latency(redis, tiny_dataset)
    test_throughput(redis, tiny_dataset)

    print("\nTesting Small Dataset")
    test_memory_utilization(redis, small_dataset)
    test_response_latency(redis, small_dataset)
    test_throughput(redis, small_dataset)

    print("\nTesting Large Dataset")
    test_memory_utilization(redis, large_dataset)
    test_response_latency(redis, large_dataset)
    test_throughput(redis, large_dataset)