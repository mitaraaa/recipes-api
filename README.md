# 🍳 Recipes API

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5d48f7c13cf24e0ab01a638771a6322a)](https://app.codacy.com/gh/mitaraaa/recipes-api?utm_source=github.com&utm_medium=referral&utm_content=mitaraaa/recipes-api&utm_campaign=Badge_Grade_Settings)

![GitHub](https://img.shields.io/github/license/mitaraaa/recipes-api)
![CodeFactor](https://www.codefactor.io/repository/github/mitaraaa/recipes-api/badge)

This application hosts database related API for Python course final project.

## Installation

```sh
pip install -r requirements.txt
```

## Usage

```sh
flask run
```
or  
```sh
python -m flask run
```

## API Routes
Get all recipes  
```
GET /
```
Get recipe by ID  
```
GET /recipe/<recipe_id>
```
Get recipes by name  
```
GET /recipe?name=<name>
```
Get account data by ID
```
GET /user/<user_id>
```
Get account data by login
```
GET /user/<login>
```
Create new account (requires form-data)
```
POST /signup
```
Log into account (requires login and password in form-data)
```
POST /login
```
**[AUTH]** Get own account data 
```
GET /account
```
**[AUTH]** Add recipe (requires recipe JSON in body)
```
POST /recipe/add
```
**[AUTH]** Add recipe to favorites
```
POST /favorite/add/<recipe_id>
```
**[AUTH]** Remove recipe from favorites
```
POST /favorite/remove/<recipe_id>
```
**[AUTH]** Log out from account
```
POST /logout
```
## Examples

### API Call

```
GET /recipes/1
```

### Response

```json
{
    "recipe_id": 1,
    "name": "Double Layer Pumpkin Cheesecake",
    "description": "This pumpkin cheesecake is a great alternative to traditional cheesecake — especially for pumpkin pie fans! A thick, creamy cheesecake base topped with a layer of spiced pumpkin cheesecake filling sits on a graham cracker crust in this easy layered holiday dessert. Two flavors of cheesecake in every bite! Serve with a scoop of vanilla ice cream or a dollop of whipped cream.",
    "image": "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%2F8425283.jpg&q=60&c=sc&orient=true&poi=auto&h=512",
    "ingridients": [
        "2 (8 ounce) packages cream cheese, softened",
        "½ cup white sugar",
        "½ teaspoon vanilla extract",
        "2 large eggs",
        "1 (9 inch) prepared graham cracker crust",
        "½ cup pumpkin puree",
        "½ teaspoon ground cinnamon",
        "1 pinch ground cloves, or more to taste",
        "1 pinch ground nutmeg, or more to taste"
    ],
    "directions": [
        "Preheat the oven to 325 degrees F (165 degrees C).",
        "Make cheesecake layer: Beat cream cheese, sugar, and vanilla in a large bowl with an electric mixer until smooth. Add eggs, one at a time, blending well after each addition. Spread 1 cup batter in the graham cracker crust.",
        "Make pumpkin layer: Add pumpkin puree, cinnamon, cloves, and nutmeg to the remaining batter; stir gently until well blended. Carefully spread on top of plain cheesecake batter in the crust.",
        "Bake in the preheated oven until the edges are puffed and the surface is firm except for a small spot in the center that jiggled when the pan is gently shaken, 35 to 40 minutes.",
        "Remove from the oven, set on a wire rack, and cool to room temperature, 1 to 2 hours.",
        "Refrigerate for at least 3 hours before serving, preferably overnight."
    ],
    "cooking_time": 2100,
    "calories": 415,
    "posted_at": "2022-11-09T01:37:55.409967",
    "author_id": 1
}
```

### Fields in API response

`name` - Name of recipe  
`description` - Small description of given recipe (optional)  
`image` - URL for header image  
`ingridients` - List of ingridients  
`directions` - List of steps required for cooking  
`cooking_time` - Time to cook with given recipe (seconds)  
`calories` - Amount of calories in one serving (calories)  
`posted_at` - Local timestamp  
`author_id` - Author's ID

## License
[MIT](https://choosealicense.com/licenses/mit/)