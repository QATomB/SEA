from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired
from database.models.item_transit import Locations
from database.models.employee import employee
from wtforms_sqlalchemy.fields import QuerySelectField
from database.db import db

def all_employees():
    employees: list[employee] = db.session.query(employee).all()
    for e in employees:
        yield e

class ItemTransitForm(FlaskForm):
    item_id = IntegerField('Item Id', validators=[DataRequired()])
    move_date = DateTimeLocalField('Move Time', validators=[DataRequired()])
    from_loc = SelectField('Start location', choices=[(choice.name, choice.name) for choice in Locations], validators=[DataRequired()])
    to_loc = SelectField('End location', choices=[(choice.name, choice.name) for choice in Locations], validators=[DataRequired()])
    employee_id = QuerySelectField('Assigned Employee\'s Employee ID', query_factory=all_employees, validators=[DataRequired()])
    submit = SubmitField('Add Item Type')
