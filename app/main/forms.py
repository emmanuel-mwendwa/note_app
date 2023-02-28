from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class AddNoteForm(FlaskForm):
    note = TextAreaField("",validators=[DataRequired(), Length(1, 10000)])
    submit = SubmitField('Add Note')

class EditNoteForm(FlaskForm):
    note = TextAreaField("",validators=[DataRequired(), Length(1, 10000)])
    submit = SubmitField('Update Note')