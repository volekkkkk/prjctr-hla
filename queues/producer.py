#!/usr/bin/env python3
import random
import string
import greenstalk
import redis

MESSAGE_SIZE = 65535

def generate_random_string(length):
   letters = string.ascii_lowercase + string.digits
   return ''.join(random.choice(letters) for i in range(length))

def main():
    redis_aof = redis.Redis("redis-aof")
    redis_rdb = redis.Redis("redis-aof")
    beanstalk = greenstalk.Client(("localhost", 11300))

    beanstalk.use("default")
    
    for _ in range(100000):
        beanstalk.put(generate_random_string(MESSAGE_SIZE))

if __name__ == "__main__":
    main()
