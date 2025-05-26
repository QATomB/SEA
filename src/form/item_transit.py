from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from database.models.item import Quality

# class ItemForm(FlaskForm):
#     item_id = StringField('Item Type', validators=[DataRequired()])
    
#     move_date = DateTimeField('Move Time', validators=[DataRequired()])
#     from_loc: Mapped[Locations] = mapped_column(Enum(Locations))
#     to_loc: Mapped[Locations] = mapped_column(Enum(Locations))
#     employee_id: Mapped[str] = mapped_column(String, ForeignKey("employee.employee_id"))

#     submit = SubmitField('Add Item Type')
