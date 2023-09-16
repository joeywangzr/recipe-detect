"""
Main backend application run.
"""
from dotenv import load_dotenv
import os
from os.path import join, dirname
from flask import Flask

from database import db
from routes import recipe_routes

app = Flask(__name__)
app.register_blueprint(recipe_routes)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8080, debug=True)