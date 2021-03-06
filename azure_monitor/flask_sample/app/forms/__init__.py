from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    add_input = StringField('To Do', validators=[DataRequired()])
    mark_submit = SubmitField('Mark As Complete')
    valid_submit = SubmitField('Save to File')
