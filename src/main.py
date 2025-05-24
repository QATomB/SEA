from flask import Flask, jsonify, redirect, render_template, request, url_for, flash
from database.db import db, InitialiseDatabase
from database.models.item_type import item_type
from database.models.item import item
from database.models.employee import employee
from database.models.item_transit import item_transit
import json
import os
import form as Forms


DEBUG_ROUTE = "/api"

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = "os.environ.get('SECRET_KEY')"
InitialiseDatabase(app=app)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"

@app.route(DEBUG_ROUTE + "/all_employees")
def get_all_employees():
    all_employees = '{'
    for e in employee.query.all():
        all_employees += '{"employee_id" : "' + e.employee_id + '", "name" : "' + e.name + '"},'
    all_employees += "}"
    return jsonify(all_employees)

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee_record():
    form = Forms.EmployeeForm()
    if form.validate_on_submit():
        flash(f'Requested addition of employee record named: {form.name}')
        emp = employee(employee_id = form.employee_id.data, name=form.name.data)
        db.session.add(emp)
        db.session.commit()
        return redirect(DEBUG_ROUTE + "/all_employees")
    return render_template('add_employee.html', title="Add Employee", form=form)

# @app.route(DEBUG_ROUTE + "move_item")
# def add_item_movement_log():
