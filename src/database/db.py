from flask import Flask
from sqlalchemy import Integer, String
from database.base_items import db
from database.models.employee import employee

# Simple function to initialise a connection to the db and create the models/tables if they don't already exist
def InitialiseDatabase(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()