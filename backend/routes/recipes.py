"""
Routes for querying and saving recipes.
"""

from flask import Blueprint, request, Response

from database import db, Recipe

recipe_routes = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipe_routes.route('/', methods=["GET"])
def get_all_recipes():
    query = db.select(Recipe)
    recipes = [r.to_json() for r in list(db.session.execute(query).scalars())]
    return recipes

@recipe_routes.route('/insert', methods=["POST"])
def insert_recipes():
    data = request.get_json()
    for raw in data:
        recipe_name = raw.get("name")
        recipe_ingredients = raw.get("ingredients") if raw.get("ingredients") is not None else []
        recipe_steps = raw.get("steps") if raw.get("steps") is not None else ""
        if recipe_name is None or recipe_name == '':
            return Response({"status": "error", "error": "Recipe name cannot be null."}, status=400)
        recipe = Recipe(
            name=recipe_name,
            ingredients=recipe_ingredients,
            steps=recipe_steps
        )
        db.session.add(recipe)

    db.session.commit()
    return Response({"status": "success", "data": data}, status=200)

@recipe_routes.route('/delete', methods=["DELETE"])
def delete_recipes():
    data = request.get_json()
    deleted = []
    print(data)
    for raw in data:
        delete_id = raw.get("id")
        recipe = db.session.query(Recipe).filter(Recipe.id == delete_id).first()
        print(recipe)
        if recipe is not None:
            deleted.append(raw)
            db.session.delete(recipe)
    db.session.commit()
    return {"status": "success", "data": deleted}