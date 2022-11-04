# 🍳 Recipes API

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

## Examples

### How to make an API call
Get all recipes  
```
GET /get
```
Get recipe by ID  
```
GET /get?id=1
```
Get recipes by name  
```
GET /get?name=Duck
```
Add recipe (requires recipe JSON in body)  
```
POST /add
```

### Response

```json
{
  "calories": 504,
  "cooking_time": 1800,
  "description": "I can't stand those instant banana puddings. This one is old and authentic!",
  "directions": [
    "Preheat oven to 350 degrees F (175 degrees C).",
    "Line the bottom and sides of a 9-inch pie plate with a layer of alternating vanilla wafer crumbs and banana slices.",
    "To Make Pudding: In a medium saucepan, combine 1 1/2 cups sugar with flour. Mix well, then stir in half the milk. Beat egg yolks and whisk into sugar mixture. Add remaining milk and butter or margarine.",
    "Place mixture over low heat and cook until thickened, stirring frequently. Remove from heat and stir in vanilla extract. Pour half of pudding over vanilla wafer and banana layer while still hot.",
    "Make another layer of alternating vanilla wafers and banana slices on top of pudding layer. Pour remaining pudding over second wafer and banana layer.",
    "To Make Meringue: In a large glass or metal bowl, beat egg whites until foamy. Gradually add 1/4 cup sugar, continuing to beat until whites are stiff. Spread meringue into pie pan, making sure to completely cover pudding layer.",
    "Bake in preheated oven for 15 minutes, just until meringue is browned. Chill before serving."
  ],
  "id": 1,
  "image": "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%2F7504588.jpg&q=60&c=sc&orient=true&poi=auto&h=512",
  "ingridients": [
    "2 cups vanilla wafer crumbs",
    "3 bananas, sliced into 1/4 inch slices",
    "1 ½ cups white sugar",
    "¼ cup all-purpose flour",
    "2 cups milk",
    "3 egg yolks",
    "2 teaspoons butter",
    "2 teaspoons vanilla extract",
    "3 egg whites",
    "¼ cup white sugar"
  ],
  "name": "Homemade Banana Pudding Pie"
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

## License
[MIT](https://choosealicense.com/licenses/mit/)