import psycopg2
import psycopg2.extras


class Recipe:
    """
    Python object for recipe's JSON representation
    """

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
        """
        Called if there is need to call `json.dumps()` on this object
        """
        return self.__dict__


class Database:
    class DatabaseException(Exception):
        pass

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
        """
        Returns recipes found by given criteria (`name` or `recipe_id`)

        NOTE: Prefers `recipe_id` over `name` when both are provided

        Returns all recipes if no criteria provided
        """
        if recipe_id:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM recipes WHERE id=%s;", (recipe_id,)
                )

                if recipe := cursor.fetchone():
                    return Recipe(**dict(zip(self.__recipe_zip, recipe)))

        else:
            all_query = "SELECT * FROM recipes;"
            name_query = (
                "SELECT * FROM recipes WHERE LOWER(name) LIKE LOWER(%s);"
            )

            with self.connection.cursor() as cursor:
                cursor.execute(
                    name_query if name else all_query,
                    (f"%{name}%",) if name else None,
                )

                if recipes := cursor.fetchall():
                    return [
                        Recipe(**dict(zip(self.__recipe_zip, recipe)))
                        for recipe in recipes
                    ]

        return None

    def add(self, recipe: Recipe):
        """
        Adds given `recipe` object to database
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    (
                        "INSERT INTO recipes "
                        "(name, description, image, ingridients, "
                        "directions, cooking_time, calories)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    ),
                    recipe.values(),
                )
            except self.connection.Error:
                raise self.DatabaseException
