#!/usr/bin/env python3
import datetime
import os
import sys

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017", username="admin", password="admin")
try:
    client.admin.command('ismaster')
except:
    print("Cant connect to Mongo")
    sys.exit(1)

@app.route('/')
def main():
    db = client.test_db
    recs = db.records

    record = {
        "author": "me",
        "log_time": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    rec_id: int
    try:
        rec_id = recs.insert_one(record).inserted_id
    except Exception as e:
        print(f"Error: {e}")
        return "Cannot insert value"
    return f"New value inserted {rec_id}!\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("APP_SERVER_PORT", 9090), debug=True)
