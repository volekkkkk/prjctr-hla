#!/usr/bin/env python3
import random
import string
import greenstalk
import redis

MESSAGE_SIZE = 65535
MESSAGE_CNT = 1000


def generate_random_string(length):
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for i in range(length))


def main():
    redis_aof = redis.Redis("redis-aof")
    redis_aof = redis.Redis("localhost", 6380)
    redis_rdb = redis.Redis("redis-aof")
    redis_rdb = redis.Redis("localhost", 6379)
    beanstalk = greenstalk.Client(("localhost", 11300))

    beanstalk.use("default")

    for _ in range(MESSAGE_CNT):
        task_body = generate_random_string(MESSAGE_SIZE)
        beanstalk.put(task_body)
        redis_rdb.lpush("TEST_QUEUE", task_body)
        redis_aof.lpush("TEST_QUEUE", task_body)


if __name__ == "__main__":
    main()
