import psycopg2
import psycopg2.extras


class Recipe:
    name: str
    description: str
    image: str
    ingridients: list[str]
    directions: list[str]
    cooking_time: int
    calories: int

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def values(self) -> list:
        return [
            self.name,
            self.description,
            self.image,
            self.ingridients,
            self.directions,
            self.cooking_time,
            self.calories,
        ]

    def json(self):
        return self.__dict__


class Database:
    __recipe_zip = [
        "id",
        "name",
        "description",
        "image",
        "ingridients",
        "directions",
        "cooking_time",
        "calories",
    ]

    def __init__(self, **config: dict[str, str | int]) -> None:
        psycopg2.extras.register_uuid()

        self.connection = psycopg2.connect(**config)
        self.connection.autocommit = True

    def get(
        self, name: str = None, recipe_id: int = None
    ) -> Recipe | list[Recipe] | None:
        if recipe_id:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM recipes WHERE id=%s;", (recipe_id,)
                )

                if recipe := cursor.fetchone():
                    return Recipe(**dict(zip(self.__recipe_zip, recipe)))

        if name:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM recipes WHERE LOWER(name) LIKE LOWER(%s);",
                    (f"%{name}%",),
                )

                if recipes := cursor.fetchall():
                    return [
                        Recipe(**dict(zip(self.__recipe_zip, recipe)))
                        for recipe in recipes
                    ]

        return None

    def get_all(self) -> list[Recipe] | None:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM recipes;")

            if recipes := cursor.fetchall():
                return [
                    Recipe(**dict(zip(self.__recipe_zip, recipe)))
                    for recipe in recipes
                ]

        return None

    def add(self, recipe: Recipe):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO recipes (name, description, image, ingridients, directions, cooking_time, calories) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                recipe.values(),
            )
