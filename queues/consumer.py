#!/usr/bin/env python3
from hashlib import sha256
from threading import Thread
import greenstalk
import redis
import time

beanstalkd_process_counter = 0
redis_rdb_process_counter = 0
redis_aof_process_counter = 0


def process_beanstalkd_queue(client: greenstalk.Client):
    while True:
        job = client.reserve()
        if job:
            msg = sha256(job.body).hexdigest()
            print(msg)
            client.delete(job)


def process_redis_queue(redis_client: redis.Redis):
    while True:
        job = redis_client.rpop("TEST_QUEUE")
        if job:
            msg = sha256(job).hexdigest()
            print(msg)
            import sys

            sys.exit(0)
        time.sleep(1)


def main():
    with greenstalk.Client(("localhost", 11300)) as beanstalk, redis.Redis(
        "localhost", 6380
    ) as redis_aof, redis.Redis("localhost", 6379) as redis_rdb:

        beanstolkd_consumer_thread = Thread(
            name="consume_beanstalkd",
            daemon=True,
            target=process_beanstalkd_queue,
            args=(beanstalk,),
        )
        redis_rdb_consumer_thread = Thread(
            name="consume_rdb",
            daemon=True,
            target=process_redis_queue,
            args=(redis_rdb,),
        )
        redis_aof_consumer_thread = Thread(
            name="consume_aof",
            daemon=True,
            target=process_redis_queue,
            args=(redis_aof,),
        )

        # beanstolkd_consumer_thread.start()
        redis_rdb_consumer_thread.start()
        # redis_aof_consumer_thread.start()

        # beanstolkd_consumer_thread.join()
        redis_rdb_consumer_thread.join()


if __name__ == "__main__":
    main()
