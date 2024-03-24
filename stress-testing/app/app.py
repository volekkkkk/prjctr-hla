#!/usr/bin/env python3
import datetime
import os
import sys

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongo:27017", username="admin", password="admin")

def dummy_mongo_write(user: str, record: int) -> str:
    db = mongo_client.test_db
    recs = db.records

    record = {
        "user": user,
        "log_time": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    rec_id: int
    try:
        rec_id = recs.insert_one(record).inserted_id
    except Exception as e:
        app.logger().error(f"Error: {e}")
        return "Cannot insert value"
    return f"New Mongo value inserted {rec_id}!\n"

@app.post("/")
def main():
    user = request.args.get("user", type=str)
    record = request.args.get("record", type=int)
    dummy_mongo_write(user, record)
    return "New values inserted"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("APP_SERVER_PORT", 9090), debug=True)
