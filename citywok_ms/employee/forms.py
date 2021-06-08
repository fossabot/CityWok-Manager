from datetime import date

from citywok_ms.employee.models import Employee
from citywok_ms.utils import ID, SEX
from citywok_ms.utils.fields import BlankCountryField, BlankSelectField
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import (DateField, DecimalField, EmailField,
                                  IntegerField, TelField)
from wtforms.validators import (Email, InputRequired, NumberRange, Optional,
                                ValidationError)
from wtforms_alchemy import QuerySelectField
from wtforms_alchemy.utils import choice_type_coerce_factory
from wtforms_components import SelectField


class EmployeeForm(FlaskForm):
    """
    Form to create or update Employee
    """
    hide_id = HiddenField()
    first_name = StringField(label='First Name',
                             validators=[InputRequired()])
    last_name = StringField(label='Last Name',
                            validators=[InputRequired()])
    zh_name = StringField(label='Chinese Name',
                          filters=[lambda x: x or None],
                          validators=[Optional()])
    sex = BlankSelectField(label='Sex',
                           choices=SEX,
                           coerce=choice_type_coerce_factory(
                               Employee.sex.type),
                           message='---',
                           validators=[InputRequired()])
    birthday = DateField(label='Birthday',
                         validators=[Optional()])
    contact = TelField(label='Contact',
                       validators=[Optional()],
                       filters=[lambda x: x or None])
    email = EmailField(label='E-mail',
                       validators=[Optional(),
                                   Email()],
                       filters=[lambda x: x or None])
    id_type = BlankSelectField(label='ID Type',
                               validators=[InputRequired()],
                               choices=ID,
                               coerce=choice_type_coerce_factory(
                                   Employee.id_type.type),
                               message='---')
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
                                validators=[InputRequired(),
                                            NumberRange(min=0)],
                                default=635)

    remark = TextAreaField(label='Remark',
                           validators=[Optional()],
                           filters=[lambda x: x or None])

    submit = SubmitField(label='Add')
    update = SubmitField(label='Update')

    def validate_id_validity(self, id_validity):
        """
        Validate the id_validity field, check if it's still valid
        """
        if (self.id_validity.data and self.id_validity.data < date.today()):
            raise ValidationError('ID has expired')

    def validate_nif(self, nif):
        '''
        Validate the nif field, to avoid duplicate nif number
        '''
        e = Employee.query.filter_by(nif=nif.data).first()
        if nif.data and e and (e.id != self.hide_id.data):
            raise ValidationError('This NIF already existe')

    def validate_niss(self, niss):
        '''
        Validate the niss field, to avoid duplicate niss number
        '''
        e = Employee.query.filter_by(niss=niss.data).first()
        if niss.data and e and (e.id != self.hide_id.data):
            raise ValidationError('This NISS already existe')
