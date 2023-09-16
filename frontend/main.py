"""
Taipy frontend for application.
"""
import taipy
import os

from models.ingredient import Ingredient

# state
path = None
pantry = []
current_ingredient = Ingredient()

# bindings
value = None
number = None

markdown = """
# Recipede.tech

## Pantry
<|card|

Ingredient Name: <|{value}|input|label=Ingredient Name|on_change=on_ingredient_change|>
<|Add Ingredient|button|on_action=add_ingredient|>
|>

Flyer: <|{path}|file_selector|label=Upload Flyer|extensions=.png,.jpg|on_action=load_file|>

        
"""
# state modification
def on_ingredient_change(state):
    current_ingredient.set_name(state.value)

def add_ingredient():
    to_add = Ingredient.from_existing(current_ingredient)
    pantry.append(to_add)
    current_ingredient.reset()
    print(pantry)

def load_file(state):
    mypath = state.path
    print(mypath)

taipy.Gui(page=markdown).run(
    title="Let us cook",
    host='0.0.0.0',
    port=os.environ.get('PORT', '5000'),
)