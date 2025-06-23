import unittest
import time
from server import parse_resp, is_expired, data_store, expiry_store

class RedisCloneTests(unittest.TestCase):

    def test_parse_resp(self):
        raw = "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"
        parsed = parse_resp(raw)
        self.assertEqual(parsed, ["GET", "key"])

    def test_expiry_check(self):
        key = "temp"
        data_store[key] = "value"
        expiry_store[key] = time.time() - 10 
        self.assertTrue(is_expired(key))
        self.assertNotIn(key, data_store)
        self.assertNotIn(key, expiry_store)

    def test_not_expired(self):
        key = "active"
        data_store[key] = "123"
        expiry_store[key] = time.time() + 10
        self.assertFalse(is_expired(key))

    def test_set_and_get(self):
        key, value = "username", "rehan"
        data_store[key] = value
        self.assertIn(key, data_store)
        self.assertEqual(data_store[key], value)

    def test_expire_and_ttl(self):
        key = "session"
        data_store[key] = "xyz"
        expiry_store[key] = time.time() + 5

        remaining =int(expiry_store[key] - time.time())
        self.assertGreaterEqual(remaining, 0)

    def test_selete_key(self):
        key = "tempkey"
        data_store[key] = "123"
        self.assertIn(key, data_store)

        data_store.pop(key, None)
        expiry_store.pop(key, None)
        self.assertNotIn(key, data_store) 


if __name__ == '__main__':
    unittest.main()
