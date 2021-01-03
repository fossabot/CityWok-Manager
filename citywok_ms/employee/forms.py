from datetime import date

from citywok_ms.fields import BlankCountryField, BlankSelectField
from citywok_ms.models import Employee
from citywok_ms.utils import ID, SEX
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import (DateField, DecimalField, EmailField,
                                  IntegerField, TelField)
from wtforms.validators import (Email, InputRequired, NumberRange, Optional,
                                ValidationError)
from wtforms_alchemy import CountryField, QuerySelectField
from wtforms_components import SelectField


class EmployeeForm(FlaskForm):
    first_name = StringField(label='First Name',
                             validators=[InputRequired()])
    last_name = StringField(label='Last Name',
                            validators=[InputRequired()])
    zh_name = StringField(label='Chinese Name',
                          default='-',
                          validators=[Optional()])
    sex = BlankSelectField(label='Sex',
                           choices=[('', '---')]+SEX,
                           message='---',
                           validators=[InputRequired()])
    birthday = DateField(label='Birthday',
                         validators=[Optional()],
                         render_kw={'type': 'date'})
    contact = TelField(label='contact',
                       validators=[Optional()],
                       filters=[lambda x: x or None])
    email = EmailField(label='E-mail',
                       validators=[Optional(),
                                   Email()],
                       filters=[lambda x: x or None])
    id_type = SelectField(label='ID Type',
                          validators=[InputRequired()],
                          choices=[('', '---')]+ID)
    id_number = StringField(label='ID Number',
                            validators=[InputRequired()])
    id_validity = DateField(label='ID Validity',
                            validators=[InputRequired()])
    nationality = BlankCountryField(label='Nationality',
                                    message='---',
                                    validators=[InputRequired()])
    nif = IntegerField(label='NIF',
                       validators=[Optional()])
    niss = IntegerField(label='NISS',
                        validators=[Optional()])
    employment_date = DateField(label='Employment Date',
                                validators=[Optional()])
    total_salary = DecimalField(label='Total Salary',
                                validators=[InputRequired(),
                                            NumberRange(min=0)])
    taxed_salary = DecimalField(label='Taxed Salary',
                                validators=[Optional(),
                                            NumberRange(min=0)],
                                default=635)

    remark = TextAreaField(label='Remark',
                           validators=[Optional()],
                           filters=[lambda x: x or None])

    submit = SubmitField(label='Add')

    def validate_id_validity(self, id_validity):
        if (self.id_validity.data and self.id_validity.data < date.today()):
            raise ValidationError('ID has expired')

    def validate_nif(self, nif):
        e = Employee.query.filter_by(nif=nif.data).first()
        if nif.data and e and (e.id != self.ID.data):
            raise ValidationError('This NIF already existe')

    def validate_niss(self, niss):
        e = Employee.query.filter_by(niss=niss.data).first()
        if niss.data and e and (e.id != self.ID.data):
            raise ValidationError('This NISS already existe')
