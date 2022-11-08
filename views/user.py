import json
import bcrypt
from http import HTTPStatus

from flask import Blueprint, request, url_for, redirect
from flask_login import login_required, current_user, login_user, logout_user

from models import User, db
from utils import message

user_app = Blueprint("users", __name__)


@user_app.route("/account")
@login_required
def account():
    return json.dumps(current_user.json())


@user_app.route("/user/<user_id>")
def get_user_by_id(user_id: int):
    if not user_id:
        if current_user.authenticated:
            return redirect(url_for("account"))

        return message("Invalid request", HTTPStatus.BAD_REQUEST)

    user = db.session.query(User).filter_by(user_id=user_id).first()

    return json.dumps(user.json())


@user_app.route("/user/<login>")
def get_user_by_login(login: str):
    if not login:
        if current_user.authenticated:
            return redirect(url_for("account"))

        return message("Invalid request", HTTPStatus.BAD_REQUEST)

    user = db.session.query(User).filter_by(login=login).first()

    return json.dumps(user.json())


@user_app.route("/login", methods=["GET", "POST"])
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


@user_app.route("/signup", methods=["POST"])
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


@user_app.route("/logout")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return message("Logged out", HTTPStatus.OK)
