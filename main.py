import requests
import json

kinds = [
    ['garlic', []],
    ['sugar', []],
    ['ginger', []],
    ['milk', []],
    ['bread', []],
    ['fennel', []],
    ['nut', []],
    ['tomato', []],
    ['egg', []],
    ['mustard', []],
    ['onion', []],
    ['paprika', []],
]

url = 'https://www.themealdb.com/api/json/v1/1/list.php?i=list'
r = requests.get(url, auth=('user', 'pass'))
all_ingredients_json = r.json()


def extract(m): return {
    'name': m['strIngredient'],
    'id': str(m['idIngredient'])
}


all_ingredients = list(map(extract, all_ingredients_json['meals']))


def find_matching_kinds(ingredient):
    ingredient_l = ingredient['name'].lower()
    return list(filter(
        lambda kind: ingredient_l in kind[0] or kind[0] in ingredient_l,
        kinds
    ))


def run_classify(ingredients):
    # classify each ingredient to either existing or its own category
    for ingredient in ingredients:
        matching_kinds = find_matching_kinds(ingredient)  # TODO: iffy
        if len(matching_kinds) > 0:
            # existing kind, append to first matching
            first_matching = matching_kinds[0]
            idx = kinds.index(first_matching)
            kinds[idx][1].append(ingredient)
        elif len(matching_kinds) == 0:
            # create new kind
            name = ingredient['name']
            kinds.append([name.lower(), [ingredient]])


print("RUNNING INGREDIENTS CLASSIFICATION...")
run_classify(all_ingredients)
print("FINISHED RUNNING INGREDIENTS CLASSIFICATION")

kinds_map = {
    "map": list(map(lambda k: { "name": k[0], "ingredients": k[1] }, kinds))
}
kinds_json = json.loads(str(kinds_map).replace("'", '"'))
kinds_json_formatted = json.dumps(kinds_json, indent=2)

print("WRITING MAP TO FILE...")
with open("out.json", "w") as file:
    file.write(kinds_json_formatted)