class Recipe:
    def __init__(self, name=None, ingredients=[], steps=[]):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps

    def to_json(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "steps": self.steps
        }
