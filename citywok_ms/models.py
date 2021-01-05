from citywok_ms import db
from citywok_ms.utils import SEX, ID
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, Date, Text, Boolean, Numeric
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import ChoiceType, CountryType
from decimal import Decimal


class SqliteDecimal(TypeDecorator):
    # This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
    # from Python to Integers which is later stored in Sqlite database.
    impl = Integer

    def __init__(self, scale):
        # It takes a 'scale' parameter, which specifies the number of digits
        # to the right of the decimal point of the number in the column.
        TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(self, value, dialect):
        # e.g. value = Column(SqliteDecimal(2)) means a value such as
        # Decimal('12.34') will be converted to 1234 in Sqlite
        if value is not None:
            value = int(Decimal(value) * self.multiplier_int)
        return value

    def process_result_value(self, value, dialect):
        # e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None:
            value = (Decimal(value) /
                     self.multiplier_int).quantize(Decimal(10) ** -self.scale)
        return value


class Employee(db.Model):
    id = Column(Integer,
                primary_key=True)
    first_name = Column(String,
                        nullable=False)
    last_name = Column(String,
                       nullable=False)
    zh_name = Column(String)
    sex = Column(ChoiceType(SEX, String()),
                 nullable=False)
    birthday = Column(Date)
    contact = Column(String)
    email = Column(String)
    id_type = Column(ChoiceType(ID),
                     nullable=False)
    id_number = Column(String,
                       nullable=False)
    id_validity = Column(Date,
                         nullable=False)
    nationality = Column(CountryType,
                         nullable=False)
    nif = Column(Integer, unique=True)
    niss = Column(Integer, unique=True)
    employment_date = Column(Date)
    total_salary = Column(SqliteDecimal(2))
    taxed_salary = Column(SqliteDecimal(2))
    remark = Column(Text)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f'Employee({self.id}: {self.first_name} {self.last_name})'

    @validates('sex')
    def validate_sex(self, key, sex):
        if sex not in [s[0] for s in SEX]:
            raise ValueError(f'"{sex}" not in SEX set')
        else:
            return sex
