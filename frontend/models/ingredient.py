

class Ingredient:
    def __init__(self, name = "", price = None, discounted_price = None):
        self.name = name
        self.price = price
        self.discounted_price = price if discounted_price is None else discounted_price
    
    def set_price(self, new_price: float):
        self.price = round(new_price, 2)
    
    def set_name(self, new_name: str):
        self.name = new_name.strip(" .,")
    
    def reset(self):
        self.name = ""
        self.price = None
        self.discounted_price = None
    
    def __repr__(self) -> str:
        return f"{self.name} - ${self.price} base, ${self.discounted_price} discounted"
    
    @staticmethod
    def from_existing(ingredient: 'Ingredient'): 
        return Ingredient(ingredient.name, ingredient.price, ingredient.discounted_price)