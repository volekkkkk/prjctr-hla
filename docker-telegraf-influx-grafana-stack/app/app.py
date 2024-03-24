#!/usr/bin/env python3
import datetime
import os
import sys

from elasticsearch import Elasticsearch
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongo:27017", username="admin", password="admin")
es_client = Elasticsearch(["http://elasticsearch:9200"])


def dummy_mongo_write():
    db = mongo_client.test_db
    recs = db.records

    record = {
        "author": "me",
        "log_time": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    rec_id: int
    try:
        rec_id = recs.insert_one(record).inserted_id
    except Exception as e:
        app.logger().error(f"Error: {e}")
        return "Cannot insert value"
    return f"New Mongo value inserted {rec_id}!\n"

def dummy_es_write():
    doc = {
        "author": "you",
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    resp = es_client.index(index="test-index", id=1, document=doc)
    app.logger.info(resp["result"])

def dummy_es_read():
    resp = es_client.get(index="test-index", id=1)
    app.logger.info(resp["_source"])

    es_client.indices.refresh(index="test-index")

    resp = es_client.search(index="test-index", query={"match_all": {}})
    app.logger.info("Got {} hits:".format(resp["hits"]["total"]["value"]))
    for hit in resp["hits"]["hits"]:
        app.logger.info("{timestamp} {author}".format(**hit["_source"]))



@app.route("/")
def main():
    dummy_mongo_write()
    dummy_es_write()
    dummy_es_read()
    return "New values inserted"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("APP_SERVER_PORT", 9090), debug=True)
