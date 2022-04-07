from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch


es_client = Elasticsearch(
    "http://127.0.0.1:9200",
    http_auth=["elastic", "changeme"],
)


# es_client.delete(index="assignment", ignore=404, id="1")

print(es_client.ping())

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def index():
    results = es_client.get(index="assignment", id="test1")
    return jsonify(results["_source"])


@app.route("/insert_data", methods=["POST"])
def insert_data():
    id = request.json["id"]
    title = request.json["title"]
    description = request.json["description"]
    email = request.json["email"]
    tags = request.json["tags"]

    data = {
        "id": id,
        "title": title,
        "description": description,
        "email": email,
        "tags": tags,
    }
    print(data)
    result = es_client.index(index="assignment", id=id, body=data)

    print(result)

    return jsonify(result)


@app.route("/search", methods=["POST"])
def search():
    keyword = request.args["keyword"]
    print(keyword)

    body = {"query": {"multi_match": {"query": keyword, "fields": ["title", "tags"]}}}

    res = es_client.search(index="assignment", body=body)

    return jsonify(res["hits"]["hits"])


if __name__ == "__main__":
    app.run(port=5000, debug=True)
