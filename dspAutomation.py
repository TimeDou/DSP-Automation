import json


def getRecipes(filename: str) -> dict:
    rst = dict()
    with open(filename, 'r') as f:
        data = json.load(f)
    recipes = data['recipes']
    for recipe in recipes:
        components = recipe["in"]
        val = []
        for component in components:
            val.append(component + "-i")
        rst[recipe["id"]] = val
    return rst


def itemizeRecipes(recipes: dict):
    inSet = set()
    outSet = set()
    for key, value in recipes.items():
        outSet.add(key)
        for item in value:
            inSet.add(item)
    inSet2int = {symbol: i for i, symbol in enumerate(inSet)}
    outSet2int = {symbol: i for i, symbol in enumerate(outSet)}
    new_recipes = {outSet2int[key]: [inSet2int[value] for value in values] for key, values in recipes.items()}
    return new_recipes, inSet2int, outSet2int


def relationTable(recipes: dict, inSet: dict, outSet: dict) -> list:
    rst = [[0 for _ in range(len(outSet))] for _ in range(len(inSet))]
    for key, values in recipes.items():
        for value in values:
            rst[value][key] = 1
    return rst
