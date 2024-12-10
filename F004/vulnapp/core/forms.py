from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import SubmitField

class UploadForm(FlaskForm):
    new_file = FileField('New File: ', validators=[FileAllowed(['jpg', 'png'], 'Images Only'), FileRequired()])
    submit = SubmitField('Upload')
