from flask import Flask, jsonify, redirect, render_template, request, url_for
from database.example_model import User
from src.database.db import db, InitialiseDatabase

app: Flask = Flask(__name__)
InitialiseDatabase(app=app)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"