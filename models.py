import bcrypt
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id: int = db.Column(db.Integer, primary_key=True)
    login: str = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    first_name: str = db.Column(db.Text, nullable=False)
    last_name: str = db.Column(db.Text, nullable=False)
    image: str = db.Column(db.Text, nullable=True)
    authenticated: bool = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.ARRAY(db.Integer))

    def verify(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        return self.login

    def json(self):
        return {
            "user_id": self.user_id,
            "login": self.login,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "image": self.image,
            "favorite": self.favorite,
        }


class Recipe(db.Model):
    """
    Recipe model for SQLAlchemy
    """

    __tablename__ = "recipes"

    recipe_id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Text, nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    image: str = db.Column(db.Text, nullable=False)
    ingridients: list[str] = db.Column(db.ARRAY(db.Text))
    directions: list[str] = db.Column(db.ARRAY(db.Text))
    cooking_time: int = db.Column(db.Integer)
    calories: int = db.Column(db.Integer)
    posted_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column(db.Integer)

    def json(self) -> dict:
        return {
            "recipe_id": self.recipe_id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "ingridients": self.ingridients,
            "directions": self.directions,
            "cooking_time": self.cooking_time,
            "calories": self.calories,
            "posted_at": self.posted_at.isoformat(),
            "author_id": self.author_id,
        }
