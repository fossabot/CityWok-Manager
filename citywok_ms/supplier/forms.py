from citywok_ms.models import Supplier
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import (DateField, DecimalField, EmailField,
                                  IntegerField, TelField)
from wtforms.validators import (Email, InputRequired, NumberRange, Optional,
                                ValidationError)


class SupplierForm(FlaskForm):
    hide_id = HiddenField()
    name = StringField(label='Company Name',
                       validators=[InputRequired()])
    abbreviation = StringField(label='Abbreviation',
                               validators=[Optional()])
    principal = StringField(label='Principal',
                            validators=[InputRequired()])
    contact = TelField(label='Contact',
                       validators=[Optional()])

    email = EmailField(label='E-mail',
                       validators=[Optional(),
                                   Email()])
    nif = IntegerField(label='NIF',
                       validators=[Optional()])
    iban = StringField(label='IBAN',
                       validators=[Optional()],
                       filters=[lambda x: x or None])
    address = StringField(label='Address',
                          validators=[Optional()])
    postcode = StringField(label='Postcode',
                           validators=[Optional()])
    city = StringField(label='City',
                       validators=[Optional()])

    remark = TextAreaField(label='Remark',
                           validators=[Optional()])

    submit = SubmitField(label='Add')
    update = SubmitField(label='Update')

    def validate_nif(self, nif):
        s = Supplier.query.filter_by(nif=nif.data).first()
        if nif.data and s and (s.id != self.hide_id.data):
            raise ValidationError('This NIF already existe')

    def validate_iban(self, iban):
        s = Supplier.query.filter_by(iban=iban.data).first()
        if iban.data and s and (s.id != self.hide_id.data):
            raise ValidationError('This IBAN already existe')
