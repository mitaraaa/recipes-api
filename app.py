import os
import json
import bcrypt
from http import HTTPStatus
from flask import Flask, request, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)

from models import Recipe, User


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(login: str):
    return db.session.query(User).filter_by(login=login).first()


@app.route("/")
def get_recipes():
    return json.dumps(
        [recipe.json() for recipe in db.session.query(Recipe).all()]
    )


@app.route("/recipe/<recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id: int):
    recipe: Recipe = (
        db.session.query(Recipe).filter_by(recipe_id=recipe_id).first()
    )

    if not recipe:
        return message("Not found", HTTPStatus.NOT_FOUND)

    return json.dumps(recipe.json()), HTTPStatus.OK


@app.route("/recipe", methods=["GET"])
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


@app.route("/recipe/add", methods=["POST"])
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


@app.route("/account")
@login_required
def account():
    return json.dumps(current_user.json())


@app.route("/user/<user_id>")
def get_user_by_id(user_id: int):
    if not user_id:
        if current_user.authenticated:
            return url_for("account")

        return message("Invalid request", HTTPStatus.BAD_REQUEST)

    user = db.session.query(User).filter_by(user_id=user_id).first()

    return json.dumps(user.json())


@app.route("/user/<login>")
def get_user_by_login(login: str):
    if not login:
        if current_user.authenticated:
            return url_for("account")

        return message("Invalid request", HTTPStatus.BAD_REQUEST)

    user = db.session.query(User).filter_by(login=login).first()

    return json.dumps(user.json())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user: User = (
            db.session.query(User)
            .filter_by(login=request.form["login"])
            .first()
        )

        if not user:
            return message("No user with this login", HTTPStatus.BAD_REQUEST)

        if user.verify(request.form["password"]):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return message(f"Logged in as @{user.login}", HTTPStatus.OK)
    return message("Authorization error", HTTPStatus.UNAUTHORIZED)


@app.route("/signup", methods=["POST"])
def signup():
    existing = (
        db.session.query(User).filter_by(login=request.form["login"]).first()
    )

    if existing:
        return message("User already exists", HTTPStatus.BAD_REQUEST)

    new = User(
        login=request.form["login"],
        password=bcrypt.hashpw(
            request.form["password"].encode("utf-8"), bcrypt.gensalt()
        ),
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image=request.form["image"],
    )
    db.session.add(new)
    db.session.commit()

    return message("Successfully signed up", HTTPStatus.OK)


@app.route("/logout")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return message("Logged out", HTTPStatus.OK)


def message(message: str, code: HTTPStatus) -> tuple[str, HTTPStatus]:
    return json.dumps({"code": code, "message": message}), code


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=False)
