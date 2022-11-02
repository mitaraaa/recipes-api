import os
import json
from flask import Flask, request

from db import Recipe, Database


config = {
    "dbname": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
    "host": os.environ.get("PGHOST"),
    "port": os.environ.get("PGPORT"),
}

app = Flask(__name__)
db = Database(**config)


@app.route("/get", methods=["GET"])
def get():
    """
    Returns recipes found by given criteria (name or id).

    Returns all recipes if no criteria provided.
    """
    name = request.args.get("name")
    recipe_id = request.args.get("id")
    if __xor(name, recipe_id):
        fetched = db.get(name=name, recipe_id=recipe_id)
        if fetched:
            if type(fetched) == list:
                return json.dumps(
                    fetched, default=lambda recipe: recipe.json()
                )
            else:
                return fetched.json()

    return json.dumps(db.get_all(), default=lambda recipe: recipe.json())


@app.route("/add", methods=["POST"])
def add():
    """
    Adds JSON of recipe to database.
    """
    data = request.get_json()

    if data:
        try:
            recipe = Recipe(**data)
            db.add(recipe)

            return "OK", 200
        except Exception:
            return "Invalid object", 400

    return "Invalid object", 400


def __xor(a: str, b: str) -> bool:
    return bool(a) ^ bool(b)
