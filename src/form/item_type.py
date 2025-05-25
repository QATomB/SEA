from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ItemTypeForm(FlaskForm):
    # type_id = IntegerField('Type ID', validators=[DataRequired()])
    item_name = StringField('Item Type Name', validators=[DataRequired()])
    item_desc = StringField('Item Type Description', validators=[DataRequired()])
    submit = SubmitField('Add Item Type')