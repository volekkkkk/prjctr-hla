#!/usr/bin/env python3
import redis
import time
import random
import math
import json

class ProbabilisticCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)
        self.client.config_set("maxmemory-policy", "volatile-lru")

    def populate_redis(self, num_keys=10000, delta=1):
        for i in range(num_keys):
            ttl = random.randint(10, 100)
            self.cache_write(f"key{i}", "x" * 512, delta, ttl)
    
    def cache_read(self, key):
        cached_data = self.client.get(key)
        if cached_data:
            value, delta, expiry = json.loads(cached_data)
            return value, float(delta), float(expiry)
        return None, None, None

    def cache_write(self, key, value, delta, ttl):
        expiry = time.time() + ttl
        cached_data = json.dumps([value, delta, expiry])
        self.client.setex(key, ttl, cached_data)
    
    def x_fetch(self, key, ttl, beta=1, recompute_value=None):
        if recompute_value is None:
            raise ValueError("recompute_value function must be provided")

        value, delta, expiry = self.cache_read(key)
        current_time = time.time()
        recompute = delta and expiry and (current_time - delta * beta * math.log(random.random())) >= expiry 
        if recompute:
            print(f"Recompute value for {key}")

        if not value or recompute:
            start = current_time
            value = recompute_value()
            delta = time.time() - start
            self.cache_write(key, value, delta, ttl)

        return value

# Example usage
if __name__ == "__main__":
    cache = ProbabilisticCache()

    def recompute_value():
        # Simulate a time-consuming computation
        time.sleep(1)
        return "computed_value"
    
    cache.populate_redis()

    ttl = 10 
    beta = 1 # Tuning parameter for the probabilistic cache
   
    for i in range(10000):
        # Fetch the value again to demonstrate cache hit
        value = cache.x_fetch(f"key{i}", ttl, beta, recompute_value)

