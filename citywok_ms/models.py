import os
from datetime import datetime
from decimal import Decimal

from flask import current_app, url_for
from humanize import naturalsize
from sqlalchemy import (Boolean, CheckConstraint, Column, Date, DateTime,
                        ForeignKey, Integer, Numeric, String, Text)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import ChoiceType, CountryType
from werkzeug.datastructures import FileStorage

from citywok_ms import db
from citywok_ms.utils import ID, SEX


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

    files = relationship("EmployeeFile")

    def __repr__(self):
        return f'Employee({self.id}: {self.first_name} {self.last_name})'

    @property
    def active_files(self):
        return db.session.query(EmployeeFile).\
            filter_by(employee_id=self.id, delete_date=None).all()

    @property
    def deleted_files(self):
        return db.session.query(EmployeeFile).\
            filter(EmployeeFile.employee_id == self.id,
                   EmployeeFile.delete_date != None).all()

    @hybrid_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @validates('sex')
    def validate_sex(self, key, sex):
        if sex not in [s[0] for s in SEX]:  # test: no cover
            raise ValueError(f'"{sex}" not in SEX set')
        else:
            return sex


class Supplier(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String)
    principal = Column(String)
    contact = Column(Integer)
    email = Column(String)
    nif = Column(Integer, unique=True)
    iban = Column(String, unique=True)
    address = Column(String)
    postcode = Column(String)
    city = Column(String)
    remark = Column(Text)

    files = relationship("File")

    def __repr__(self):
        return f'Supplier({self.id}: {self.name})'

    @property
    def active_files(self):
        return db.session.query(SupplierFile).\
            filter_by(supplier_id=self.id, delete_date=None).all()

    @property
    def deleted_files(self):
        return db.session.query(SupplierFile).\
            filter(SupplierFile.supplier_id == self.id,
                   SupplierFile.delete_date != None).all()


class File(db.Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    delete_date = Column(DateTime)
    size = Column(Integer)
    remark = Column(Text)

    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'file'
    }

    def __repr__(self):
        return f'File({self.id}: {self.full_name})'

    @property
    def file_extension(self):
        return os.path.splitext(self.full_name)[1]

    @property
    def file_name(self):
        return os.path.splitext(self.full_name)[0]

    @property
    def internal_name(self):
        return f'{self.id}{self.file_extension}'

    @property
    def file_path(self):
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.internal_name)

    @property
    def size_humanized(self):
        return naturalsize(self.size, format="%.2f")

    @staticmethod
    def split_ext(file: FileStorage) -> str:
        return os.path.splitext(file.filename)[1]


class EmployeeFile(File):
    employee_id = Column(Integer, ForeignKey('employee.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'employee_file'
    }

    @property
    def owner_url(self):
        return url_for('employee.detail', employee_id=self.employee_id, _anchor='Files')

    @classmethod
    def save_file(cls, file: FileStorage, employee_id: int):
        db_file = cls(full_name=file.filename, employee_id=employee_id)
        db.session.add(db_file)
        db.session.flush()
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], db_file.internal_name))
        db_file.size = os.path.getsize(db_file.file_path)
        db.session.commit()


class SupplierFile(File):
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'supplier_file'
    }

    @property
    def owner_url(self):
        return url_for('supplier.detail', supplier_id=self.supplier_id, _anchor='Files')

    @classmethod
    def save_file(cls, file: FileStorage, supplier_id: int):
        db_file = cls(full_name=file.filename, supplier_id=supplier_id)
        db.session.add(db_file)
        db.session.flush()
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], db_file.internal_name))
        db_file.size = os.path.getsize(db_file.file_path)
        db.session.commit()
