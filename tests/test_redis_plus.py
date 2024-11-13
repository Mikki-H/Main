# tests/test_redis_plus.py
import unittest
import time
from src.main import RedisPlus

class TestRedisPlus(unittest.TestCase):
    def setUp(self):
        self.redis = RedisPlus()

    def test_string_operations(self):
        self.redis.set("test_key", "test_value")
        self.assertEqual(self.redis.get("test_key"), "test_value")

    def test_expiry(self):
        self.redis.set("temp_key", "temp_value", ex=1)
        self.assertEqual(self.redis.get("temp_key"), "temp_value")
        time.sleep(1.1)
        self.assertIsNone(self.redis.get("temp_key"))

    def test_list_operations(self):
        self.redis.lpush("list_key", "value1")
        self.redis.lpush("list_key", "value2")
        self.assertEqual(self.redis.lists.lpop("list_key"), "value2")

    def test_performance_monitoring(self):
        for i in range(100):
            self.redis.set(f"key_{i}", f"value_{i}")
            self.redis.get(f"key_{i}")

        stats = self.redis.get_stats()
        self.assertGreater(stats['operation_counts']['set'], 0)
        self.assertGreater(stats['operation_counts']['get'], 0)

if __name__ == '__main__':
    unittest.main()