from flask import Flask
from sqlalchemy import Integer, String
from src.database.base_items import db
from database.example_model import User

def InitialiseDatabase(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()