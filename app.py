import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from models import User, db
from views import recipe, user


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(login: str):
    return db.session.query(User).filter_by(login=login).first()


app.register_blueprint(recipe.recipe_app)
app.register_blueprint(user.user_app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=False)
