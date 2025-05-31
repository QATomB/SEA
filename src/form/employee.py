from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from database.models.employee import employee, AccessLevel
from wtforms.validators import DataRequired
from database.db import db

# Abstraction of query to run for QuerySelectField, returning all employees
def all_employees():
    employees: list[employee] = db.session.query(employee).all()
    for e in employees:
        yield e

# Employee creation form
class EmployeeForm(FlaskForm):
    employee_id = QuerySelectField('Employee ID', query_factory=all_employees, validators=[DataRequired()])
    access_level = SelectField("Access Level", choices=[(access.name, access.name) for access in AccessLevel], validators=[DataRequired()])
    submit = SubmitField('Update Employee Access')