#!/usr/bin/env python3
import redis
import random
from dataclasses import dataclass
from datetime import datetime

ALL_RECORDS = []

@dataclass
class Record:
    key: str
    read_cnt: int
    last_read: datetime
    ttl: int
    evicted: bool = False

def set_key(rd: redis.Redis, key: str):
    ttl: int = random.randint(10, 20)
    rd.set(name=key, value="TEST"*10, ex=ttl)
    ALL_RECORDS.append(Record(key, 0, datetime.now().strftime("%H:%M:%S.%f"), ttl))
    
def get_eviction_cnt(rd: redis.Redis) -> int:
    return len(ALL_RECORDS) - len(rd.keys())

def main():
    rd: redis.Redis = redis.Redis(host="localhost", port=6379)

    # evict_count 
    eviction_limit: int = 5 
    
    for i in range(1000):
        set_key(rd)

        if get_eviction_cnt >= eviction_limit:
            return 
    
if __name__=="__main__":
    main()
