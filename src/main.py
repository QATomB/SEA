from flask import Flask, jsonify, redirect, render_template, request, flash
from database.db import db, InitialiseDatabase
from database.models.item_type import item_type
from database.models.item import item, Quality
from database.models.employee import employee, AccessLevel
from database.models.item_transit import item_transit, Locations
from database.models.display.display_transit import DisplayTransit
from database.models.display.display_item import DisplayItem
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import form as Forms

# Initialise the .env
load_dotenv()

# Intialise the Flask instance
app: Flask = Flask(__name__)
login = LoginManager(app)
login.login_view = "login"
# Set Flask secret from .env
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Intitialise the database
InitialiseDatabase(app=app)

@login.user_loader
def load_user(user_id):
    try:
        return employee.query.filter_by(employee_id = user_id).one()
    except Exception as e:
        return None

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        name = request.form.get("name")
        password = request.form.get("password")

        if employee.query.filter_by(employee_id=employee_id).first():
            return render_template("register.html", error="Employee ID already used!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Automatically make first person admin
        access_level = AccessLevel.admin if not len(employee.query.all()) else AccessLevel.user
        new_user = employee(employee_id=employee_id, name=name, password=hashed_password, access_level=access_level)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            pass

        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        password = request.form.get("password")
        user = employee.query.filter_by(employee_id=employee_id).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# Main Dashboard page
@app.route("/")
@login_required
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
@app.route("/employee_permissions", methods=["GET", "POST"])
@login_required
def add_employee_record():
    if current_user.access_level != AccessLevel.admin:
        return redirect("/")
    form = Forms.EmployeeForm()
    if request.args.get("delete"):
        if current_user.access_level == AccessLevel.admin:
            employee.query.filter_by(employee_id=request.args.get("delete")).delete()
            db.session.commit()
            return redirect("/")
    if form.validate_on_submit():
        flash(f'Requested update of employee record with id: {form.employee_id.data}')
        emp = employee.query.filter_by(employee_id=form.employee_id.data.employee_id).one()
        emp.access_level = AccessLevel[form.access_level.data]
        db.session.commit()
        return redirect("/")
    return render_template('employee_permissions.html', title="Employee Permissions", form=form, employees=employee.query.all())

# Page to add a new item type record
@app.route("/add_item_type", methods=["GET", "POST"])
@login_required
def add_item_type_record():
    form = Forms.ItemTypeForm()
    if current_user.access_level == AccessLevel.admin:
        if request.args.get("delete"):
            item_type.query.filter_by(type_id=request.args.get("delete")).delete()
            db.session.commit()
            return redirect("/")
        elif request.args.get("update") and request.args.get("id") and request.args.get("name") and request.args.get("desc"):
            itm_typ = db.session.get(item_type, request.args.get("id"))
            if itm_typ == None:
                print(f"failed ({request.args.get('id')})")
            else:
                print("succeded")
                itm_typ.item_name = request.args.get("name")
                itm_typ.item_desc = request.args.get("desc")
                db.session.commit()
            return redirect("/")
    if form.validate_on_submit():
        flash(f'Requested addition of item type named: {form.item_name}')
        itm_type = item_type(item_name=form.item_name.data, item_desc=form.item_desc.data)
        try:
            db.session.add(itm_type)
            db.session.commit()
        except:
            pass
        return redirect("/")
    return render_template('add_item_type.html', title="Add Item Type", form=form, itemtypes=item_type.query.all())

# Page to add a new item record
@app.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item_record():
    form = Forms.ItemForm()
    if current_user.access_level == AccessLevel.admin:
        if request.args.get("delete"):
            item.query.filter_by(item_id=request.args.get("delete")).delete()
            db.session.commit()
            return redirect("/")
        elif request.args.get("update") and request.args.get("id") and request.args.get("type") and request.args.get("cond"):
            itm = db.session.get(item, request.args.get("id"))
            if itm == None:
                print(f"failed ({request.args.get('id')})")
            else:
                print("succeded")
                itm.type_id = request.args.get("type")
                itm.condition = Quality[request.args.get("cond")]
                db.session.commit()
            return redirect("/")
    if form.validate_on_submit():
        flash(f'Requested addition of item of type: {form.type_id}')
        itm = item(type_id=form.type_id.data, condition=Quality[form.condition.data])
        try:
            db.session.add(itm)
            db.session.commit()
        except:
            pass
        return redirect("/")
    all_items = item.query.all()
    all_item_types = item_type.query.all()
    formatted_items: list[DisplayItem] = []
    for itm in all_items:
        formatted_items.append(DisplayItem(
            item_id = itm.item_id,
            type_id = itm.type_id,
            type_name = item_type.query.filter_by(type_id=itm.type_id).one().item_name,
            condition = itm.condition
        ))
    return render_template('add_item.html', title="Add Item", form=form, items=formatted_items, item_types=all_item_types)

# Page to add a new item movement log
@app.route("/add_item_transit_log", methods=["GET", "POST"])
@login_required
def add_item_transit_record():
    form = Forms.ItemTransitForm()
    if form.validate_on_submit():
        flash(f'Requested addition of item transit log for item: {form.item_id}')
        itm = item_transit(item_id=form.item_id.data, move_date=form.move_date.data, from_loc=form.from_loc.data, to_loc=form.to_loc.data, employee_id=form.employee_id.data.employee_id)
        try:
            db.session.add(itm)
            db.session.commit()
        except:
            pass
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
    return render_template('add_move_item_log.html', title="Add Item Movement Log", form=form, items=formatted_items)
