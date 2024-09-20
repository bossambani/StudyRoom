from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, URL

class ResourceForm(FlaskForm):
    #file = FileField('Upload Resource', validators=[FileRequired(), FileAllowed(['pdf', 'docx', 'txt'], 'Only PDF, Docx, and Txt files are allowed')])
    #submit = SubmitField('Upload')
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link', validators=[URL()])
    description = TextAreaField('Description')
    type = SelectField('Type', choices=[('pdf', 'PDF'), ('docx', 'DOCX')])
    file = FileField('File', validators=[DataRequired()])

    