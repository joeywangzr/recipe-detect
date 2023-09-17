

class Ingredient:
    def __init__(self, name = "", price = None):
        self.name = name
        self.price = price
    
    def set_price(self, new_price: float):
        self.price = round(new_price, 2)
    
    def set_name(self, new_name: str):
        self.name = new_name.strip(" .,")
    
    def get_name(self):
        return self.name

    def reset(self):
        self.name = ""
        self.price = None
    
    def __repr__(self) -> str:
        return f"{self.name} - ${self.price}"
    
    @staticmethod
    def from_existing(ingredient: 'Ingredient'): 
        return Ingredient(ingredient.name, ingredient.price)