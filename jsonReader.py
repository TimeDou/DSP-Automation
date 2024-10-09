import json

# Load the JSON data from the file
with open('map.json', 'r') as file:
    data = json.loads(file.read())
    recipes = data["recipes"]
    new_json = []
    for recipe in recipes:
        del recipe["category"]
        del recipe["time"]
        del recipe["producers"]
        del recipe["unlockedBy"]
        new_json.append(recipe)
    data["recipes"] = new_json

# Dump the JSON data into a new file with formatted content
with open('buildings.json', 'w') as file:
    json.dump(data, file, indent=2)
