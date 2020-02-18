from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class FileUploadForm(FlaskForm):
    '''Form model for file submission inspection'''
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
