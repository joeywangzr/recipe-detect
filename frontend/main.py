"""
Taipy frontend for application.
"""
import taipy
import requests
import os

from models.ingredient import Ingredient

# state
file_path = None
path = None
pantry = []
status = []
current_ingredient = Ingredient()

# bindings
value = None
number = None

markdown = """
# Recipede.tech

## Pantry
<|card|

Ingredient Name: <|{value}|input|label=Ingredient Name    |on_change=on_ingredient_change|>
<|Add Ingredient|button|on_action=add_ingredient|>
|>

## Flyer
<|card|
Flyer: <|{path}|file_selector|label=Upload Flyer    |extensions=.png,.jpg|on_action=load_file|>
<|Let it cook|button|on_action=generate_recipes|>
|>


        
"""
# state modification
def on_ingredient_change(state):
    current_ingredient.set_name(state.value)

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


def generate_recipes():
    global file_path
    global pantry
    payload = {
        "path": file_path,
        "pantry": [p.name for p in pantry]
    }
    response = requests.post("http://localhost:8080/process", json=payload)
    data = response.json()
    result = data.get('result')
    print(result)

    print(data)

taipy.Gui(page=markdown).run(
    title="Let us cook",
    host='0.0.0.0',
    port=os.environ.get('PORT', '5000'),
)