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
    if name or recipe_id:
        fetched = db.get(name=name, recipe_id=recipe_id)
        if fetched:
            if isinstance(fetched, list):
                return json.dumps(
                    fetched, default=lambda recipe: recipe.json()
                )
            else:
                return fetched.json()

    return [], 404


@app.route("/add", methods=["POST"])
def add():
    """
    Adds recipe JSON to database.
    """
    data = request.get_json()

    if data:
        try:
            recipe = Recipe(**data)
            db.add(recipe)

            return "OK", 200
        except db.DatabaseException:
            return "Invalid object", 400

    return "Invalid object", 400
