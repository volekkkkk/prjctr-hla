#!/usr/bin/env python3
import redis
import random

EVICTION_STRATEGIES = [
    "allkeys-lru",
    "allkeys-lfu",
    "allkeys-random",
    "volatile-lru",
    "volatile-lfu",
    "volatile-random",
    "volatile-ttl",
    "noeviction",
]


def set_eviction_policy(rc: redis.Redis, policy: str):
    rc.config_set("maxmemory-policy", policy)


def populate_redis(
    rc: redis.Redis, num_keys=10000, value_size=2024, ttl_range=(10, 100)
):
    for i in range(num_keys):
        ttl = random.randint(ttl_range[0], ttl_range[1])
        rc.set(name=f"key{i}", value="x" * value_size, ex=ttl)


def monitor_evictions(client):
    info = client.info("stats")
    return info.get("evicted_keys", 0)


def main():
    rc: redis.Redis = redis.Redis(host="localhost", port=6379)
    rc.config_set("maxmemory", "10mb")

    for policy in EVICTION_STRATEGIES:
        print(f"Testing eviction policy: {policy}")
        rc.flushall()
        set_eviction_policy(rc, policy)

        evictions_old = monitor_evictions(rc)
        try:
            populate_redis(rc)
            evictions = monitor_evictions(rc)
            print(
                f"Eviction policy: {policy}, Evicted keys: {evictions - evictions_old}, Evicted keys total: {evictions}\n"
            )
            evictions_old = evictions
        except redis.exceptions.OutOfMemoryError as e:
            print(f"Error while testing eviction policy {policy}: {e}\n")


if __name__ == "__main__":
    main()
