from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class ResourceForm(FlaskForm):
    file = FileField('Upload Resource', validators=[FileRequired(), FileAllowed(['pdf', 'docx', 'txt'], 'Only PDF, Docx, and Txt files are allowed')])
    submit = SubmitField('Upload')

    