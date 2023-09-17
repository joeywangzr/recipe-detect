"""
Routes for processing an image.
"""

import os
from flask import Blueprint, request, Response

from generation.scanner import extract_flyer, is_food, extract_grocery
from generation.recipe_gen import generate_recipe, generate_llm_recipes
from image_process.process import crop_flyer

processing_routes = Blueprint('processing', __name__, url_prefix='/process')

@processing_routes.route('/', methods=["POST"])
def process_image():
    data = request.get_json()
    print(data)
    file_path = data.get("path")
    pantry = data.get("pantry")
    crop_flyer(file_path)

    groceries = []
    for file in os.listdir("./grocery"):
        file_path = os.path.join("./grocery", file).replace("\\", "/")
        if not os.path.isfile(file_path):
            continue

        flyer_string = extract_flyer(file_path)
        if not is_food(flyer_string):
            continue

        flyer_groceries = extract_grocery(flyer_string)
        groceries.append(flyer_groceries)
    
    groceries.extend(pantry)
    result = generate_llm_recipes(groceries)

    return {"result": result}