from flask import Flask, jsonify, redirect, render_template, request, url_for, flash
from database.db import db, InitialiseDatabase
from database.models.item_type import item_type
from database.models.item import item, Quality
from database.models.employee import employee
from database.models.item_transit import item_transit, Locations
from database.models.display.display_transit import DisplayTransit
from database.models.display.display_item import DisplayItem
from dotenv import load_dotenv
import os
import form as Forms

# Initialise the .env
load_dotenv()

# Intialise the Flask instance
app: Flask = Flask(__name__)
# Set Flask secret from .env
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Intitialise the database
InitialiseDatabase(app=app)

# Main Dashboard page
@app.route("/")
def dashboard():
    all_movement_records = item_transit.query.all()
    all_movements = []
    for record in all_movement_records:
        employee_record = employee.query.filter_by(employee_id=record.employee_id).one()
        formatted_employee_str = f"{employee_record.employee_id} ({employee_record.name})"
        itm = DisplayTransit(
            item_id=record.item_id,
            type=item_type.query.filter_by(type_id = item.query.filter_by(item_id=record.item_id).one().type_id).one().item_name,
            from_loc=record.from_loc,
            to_loc=record.to_loc,
            datetime_moved=record.move_date,
            overseer=formatted_employee_str
        )
        all_movements.append(itm)
    return render_template('dashboard.html', movements=all_movements)

# Page to add a new employee record
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee_record():
    form = Forms.EmployeeForm()
    if form.validate_on_submit():
        flash(f'Requested addition of employee record named: {form.name}')
        emp = employee(employee_id = form.employee_id.data, name=form.name.data)
        db.session.add(emp)
        db.session.commit()
        return redirect("/")
    return render_template('add_employee.html', title="Add Employee", form=form, employees=employee.query.all())

# Page to add a new item type record
@app.route("/add_item_type", methods=["GET", "POST"])
def add_item_type_record():
    form = Forms.ItemTypeForm()
    if form.validate_on_submit():
        flash(f'Requested addition of item type named: {form.item_name}')
        itm_type = item_type(item_name=form.item_name.data, item_desc=form.item_desc.data)
        db.session.add(itm_type)
        db.session.commit()
        return redirect("/")
    return render_template('add_item_type.html', title="Add Item Type", form=form, itemtypes=item_type.query.all())

# Page to add a new item record
@app.route("/add_item", methods=["GET", "POST"])
def add_item_record():
    form = Forms.ItemForm()
    if form.validate_on_submit():
        flash(f'Requested addition of item of type: {form.type_id}')
        itm = item(type_id=form.type_id.data, condition=Quality[form.condition.data])
        db.session.add(itm)
        db.session.commit()
        return redirect("/")
    all_items = item.query.all()
    formatted_items: list[DisplayItem] = []
    for itm in all_items:
        formatted_items.append(DisplayItem(
            item_id = itm.item_id,
            type_id = itm.type_id,
            type_name = item_type.query.filter_by(type_id=itm.type_id).one().item_name,
            condition = itm.condition
        ))
    return render_template('add_item.html', title="Add Item", form=form, items=formatted_items)

# Page to add a new item movement log
@app.route("/add_item_transit_log", methods=["GET", "POST"])
def add_item_transit_record():
    form = Forms.ItemTransitForm()
    if form.validate_on_submit():
        flash(f'Requested addition of item transit log for item: {form.item_id}')
        itm = item_transit(item_id=form.item_id.data, move_date=form.move_date.data, from_loc=form.from_loc.data, to_loc=form.to_loc.data, employee_id=form.employee_id.data.employee_id)
        db.session.add(itm)
        db.session.commit()
        return redirect("/")
    return render_template('add_move_item_log.html', title="Add Item Movement Log", form=form)
