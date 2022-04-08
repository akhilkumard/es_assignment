from flask import Flask, jsonify, request, render_template
from elasticsearch import Elasticsearch
import pandas as pd

es_client = Elasticsearch(
    "http://127.0.0.1:9200",
    http_auth=["elastic", "changeme"],
)
print(es_client.ping())

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("searchpage.html")


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
    result = es_client.index(index="assignment", id=id, body=data)
    return jsonify(result)


@app.route("/search", methods=["GET"])
def search():
    try:
        keyword = request.args.get("keyword")
        # Elastic search query for both title and tags fields
        body = {
            "query": {"multi_match": {"query": keyword, "fields": ["title", "tags"]}}
        }
        res = es_client.search(index="assignment", body=body)
        # Extracting data from matched results
        result = [i["_source"] for i in res["hits"]["hits"]]

        # Converting the Json result to csv to show it in table view
        columns = ["title", "description", "email", "tags"]
        df = pd.DataFrame(result, columns=columns)
        table = df.to_html(index=False)
        return render_template("at-leaderboard.html", table=table)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
