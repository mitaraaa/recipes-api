import json
from http import HTTPStatus

from flask import Blueprint, request
from flask_login import login_required, current_user

from models import Recipe, User, db
from utils import message


recipe_app = Blueprint("recipes", __name__)


@recipe_app.route("/")
def get_recipes():
    return json.dumps(
        [recipe.json() for recipe in db.session.query(Recipe).all()]
    )


@recipe_app.route("/recipe/<recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id: int):
    recipe: Recipe = (
        db.session.query(Recipe).filter_by(recipe_id=recipe_id).first()
    )

    if not recipe:
        return message("Not found", HTTPStatus.NOT_FOUND)

    return json.dumps(recipe.json()), HTTPStatus.OK


@recipe_app.route("/recipe", methods=["GET"])
def get_recipe():
    name: str = request.args.get("name")

    if not name:
        return message("Search query was not provided", HTTPStatus.BAD_REQUEST)

    recipes: list[Recipe] = (
        db.session.query(Recipe).filter(Recipe.name.like(f"%{name}%")).all()
    )

    if not recipes:
        return message("Not found", HTTPStatus.NOT_FOUND)

    return json.dumps([recipe.json() for recipe in recipes]), HTTPStatus.OK


@recipe_app.route("/recipe/add", methods=["POST"])
@login_required
def add_recipe():
    recipe_json: dict = request.get_json()

    if not recipe_json:
        return message("Empty JSON object", HTTPStatus.BAD_REQUEST)

    recipe_json["author_id"] = current_user.user_id

    recipe: Recipe = Recipe(**recipe_json)

    db.session.add(recipe)
    db.session.commit()

    return message("OK", HTTPStatus.OK)


@recipe_app.route("/favorite/<method>/<recipe_id>", methods=["POST"])
@login_required
def favorites(method: str, recipe_id: int):
    recipe: Recipe = (
        db.session.query(Recipe).filter_by(recipe_id=recipe_id).first()
    )

    if not recipe:
        return message("Not found", HTTPStatus.NOT_FOUND)

    user: User = (
        db.session.query(User).filter_by(user_id=current_user.user_id).first()
    )

    print(user.favorite)
    if method == "add":
        if not user.favorite:
            user.favorite = [recipe.recipe_id]
        else:
            user.favorite.append(recipe.recipe_id)
    elif method == "remove" and user.favorite:
        try:
            user.favorite.remove(recipe.recipe_id)
            print(user.favorite)
        except ValueError:
            return message("Not found", HTTPStatus.NOT_FOUND)

    db.session.add(user)
    db.session.commit()

    return message("OK", HTTPStatus.OK)
