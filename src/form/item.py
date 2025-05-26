from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from database.models.item import Quality

class ItemForm(FlaskForm):
    type_id = StringField('Item Type', validators=[DataRequired()])
    condition = SelectField("Item Condition", choices=[(choice.name, choice.value) for choice in Quality])
    submit = SubmitField('Add Item Type')
