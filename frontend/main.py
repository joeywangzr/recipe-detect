"""
Taipy frontend for application.
"""
import taipy
from taipy.gui import notify
import requests
import os
import pandas as pd

from models.ingredient import Ingredient

# state
file_path = None
path = None
pantry = []
status = []
generated_ingredients = []
data = pd.DataFrame([])
current_ingredient = Ingredient()

# bindings
value = None
number = None
show_recipe_modal = False
selected_recipe = {}
selected_name = None
selected_ingredients = []
selected_steps = []

markdown = """
# Recipede.tech

## Pantry
<|card|

Ingredient Name: <|{value}|input|label=Ingredient Name|on_change=on_ingredient_change|>
<|Add Ingredient|button|on_action=add_ingredient|>
|>

## Flyer
<|card|
Flyer: <|{path}|file_selector|label=Upload Flyer|extensions=.png,.jpg|on_action=load_file|>
<|Let it cook|button|on_action=generate_recipes|>
|>

## Recipes
<|card|
<|{data}|table|columns=Name|show_all|rebuild|on_action=on_recipe_click|>
|>

<|{show_recipe_modal}|dialog|on_action=display_recipe_modal|title=Recipe Display|labels=Save Recipe;Cancel|
<|
<|{selected_name}|>\n
Ingredients\n
Steps
|>
|>
"""
# state modification
def on_ingredient_change(state):
    current_ingredient.set_name(state.value)

def display_recipe_modal(state, action, payload):
    print("attempt")
    with state as st:
        print(st, action, payload)
        print("AMONGUS", dict(st.selected_recipe))
        data_display = dict(st.selected_recipe)
        st.show_recipe_modal = False
    

def update_ingredient_display(new_ingredients: 'list[Ingredient]'):
    global status
    status = [(("info", ingredient.name)) for ingredient in new_ingredients]

def add_ingredient():
    to_add = Ingredient.from_existing(current_ingredient)
    pantry.append(to_add)
    current_ingredient.reset()
    print(pantry)

def load_file(state):
    global file_path
    file_path = state.path

def on_recipe_click(state, var_name, action, payload):
    try:
        print(payload)
        idx = payload["index"]
        row = state.data.iloc[idx].to_dict()
        print(row)
        state.selected_recipe = row
        state.selected_name = row["Name"]
        state.selected_ingredients = row["Ingredients"]
        state.selected_steps = row["Steps"]
        state.show_recipe_modal = True
    except Exception as e:
        print("Recipe Error Click", str(e))


def generate_recipes(state):
    global file_path
    global data
    payload = {
        "path": file_path,
        "pantry": [p.name for p in pantry]
    }
    try:
        recipes_response = requests.post("http://localhost:8080/process", json=payload)
        recipe_data = recipes_response.json()
        recipes_result = recipe_data.get('result')

        recipe_display = {
            "Name": [],
            "Ingredients": [],
            "Steps": []
        }
        print(recipes_result)
        for recipe in recipes_result:
            name = recipe.get("name", "")

            ingredients = recipe.get("ingredients", [])
            steps = recipe.get("steps", [])
            print(name, ingredients)
            if name is None or name == "":
                continue
            recipe_display["Name"].append(name)
            recipe_display["Ingredients"].append(ingredients)
            recipe_display["Steps"].append(steps)
        data = pd.DataFrame(recipe_display)
        state.data = data
    except Exception as e:
        notify(state, "error", str(e))
    

taipy.Gui(page=markdown).run(
    title="Let us cook",
    host='0.0.0.0',
    port=os.environ.get('PORT', '5000'),
    use_reloader=True
)