from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from database.models.item import Quality

# Item creation form
class ItemForm(FlaskForm):
    type_id = StringField('Item Type ID', validators=[DataRequired()])
    condition = SelectField("Item Condition", choices=[(choice.name, choice.name) for choice in Quality], validators=[DataRequired()])
    submit = SubmitField('Add Item Type')
