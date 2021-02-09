from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Optional
from citywok_ms.utils import FILEALLOWED


class FileForm(FlaskForm):
    '''
    Form to upload a new File
    '''
    file = FileField(label='File',
                     validators=[FileRequired(),
                                 FileAllowed(FILEALLOWED)])


class FileUpdateForm(FlaskForm):
    '''
    Form to update information of a File
    '''
    file_name = StringField(label='File Name',
                            validators=[InputRequired()])
    remark = TextAreaField(label='Remark',
                           validators=[Optional()])
    update = SubmitField(label='Update')
