"""
All the models used to interface with CockroachDB.
"""
from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Integer, Double
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Ingredient(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Double, nullable=True)

class Recipe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ingredients: Mapped[list] = mapped_column(ARRAY(String), nullable=False)
    steps: Mapped[str] = mapped_column(String, nullable=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "steps": self.steps 
        }
