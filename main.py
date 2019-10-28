from pymongo import MongoClient
import redis
from flask import Flask, jsonify, request
import time
import json

# connecting to mongodb
client = MongoClient("localhost")
database = client["Book"]
book_collection = database.get_collection("User")

print("Mongodb client", client)
# connecting to redis db
rs = redis.Redis("localhost")

print("Redis :", rs)

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "Author": "includeamin",
        "Email": "aminjamal10@gmail.com"}
    )


@app.route("/book/add")
def add_book():
    book_collection.insert_one({"name": "A1.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "A1.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "A2.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "A2.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "B1.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "B1.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "B2.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "B2.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "C1.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "C1.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "C2.1", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})
    book_collection.insert_one({"name": "C2.2", "author": "amin jamal", "data": "1.1.96", "iso": "125478.645"})

    return jsonify({"result": "done"})


@app.route("/book")
def get_book():
    args = request.args
    name = args["name"]
    book = book_collection.find_one({"name": name})
    if book is None:
        return jsonify({"result": "book not found"})
    book.pop("_id")
    return jsonify({'result': book})


@app.route("/book/all")
def get_all():
    book_in_cache = rs.get("all-book")
    if book_in_cache:
        return jsonify(json.loads(book_in_cache))
    time.sleep(5)
    res = []
    items = book_collection.find({})
    for item in items:
        item.pop("_id")
        res.append(item)
    rs.set('all-book', json.dumps(res))
    return jsonify(res)


@app.route("/book/cache/remove")
def remove():
    rs.delete("all-book")
    return "done"


if __name__ == '__main__':
    app.run("0.0.0.0", 3000)
