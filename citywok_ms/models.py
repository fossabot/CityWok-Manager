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
        '''
        All files of the employee that is not in the trash bin
        '''
        return db.session.query(EmployeeFile).\
            filter_by(employee_id=self.id, delete_date=None).all()

    @property
    def deleted_files(self):
        '''
        All files of the employee that is in the trash bin
        '''
        return db.session.query(EmployeeFile).\
            filter(EmployeeFile.employee_id == self.id,
                   EmployeeFile.delete_date != None).all()

    @hybrid_property
    def full_name(self) -> str:
        ''' 
        Employee's full name (first + last name)
        '''
        return f'{self.first_name} {self.last_name}'

    @validates('sex')
    def validate_sex(self, key, sex):
        if sex not in [s[0] for s in SEX]:  # test: no cover
            raise ValueError(f'"{sex}" not in SEX set')
        else:
            return sex

    def update(self, form):
        '''
        Update the employee information by the given form
        '''
        form.populate_obj(self)
        db.session.commit()

    def activate(self):
        '''
        Activate the employee

        set ``self.active`` to ``True``
        '''
        self.active = True
        db.session.commit()

    def inactivate(self):
        '''
        Inactivate the employee

        set ``self.active`` to ``False``
        '''
        self.active = False
        db.session.commit()

    @classmethod
    def new(cls, form):
        '''
        Create a new Employee by the information in the given form
        '''
        employee = cls()
        form.populate_obj(employee)
        db.session.add(employee)
        db.session.commit()

    @staticmethod
    def save_file(file: FileStorage, employee_id: int):
        '''
        Save a file and associate it to the Employee
        '''
        db_file = EmployeeFile(full_name=file.filename,
                               employee_id=employee_id)
        db.session.add(db_file)
        db.session.flush()
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], db_file.internal_name))
        db_file.size = os.path.getsize(db_file.file_path)
        db.session.commit()


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
        '''
        All files of the supplier that is not in the trash bin
        '''
        return db.session.query(SupplierFile).\
            filter_by(supplier_id=self.id, delete_date=None).all()

    @property
    def deleted_files(self):
        '''
        All files of the supplier that is in the trash bin
        '''
        return db.session.query(SupplierFile).\
            filter(SupplierFile.supplier_id == self.id,
                   SupplierFile.delete_date != None).all()

    def update(self, form):
        '''
        Update the Supplier's information by given form
        '''
        form.populate_obj(self)
        db.session.commit()

    @classmethod
    def new(cls, form):
        '''
        Create a new Supplier by the information in the given form
        '''
        supplier = cls()
        form.populate_obj(supplier)
        db.session.add(supplier)
        db.session.commit()

    @staticmethod
    def save_file(file: FileStorage, supplier_id: int):
        '''
        Save a file and associate it to the Supplier
        '''
        db_file = SupplierFile(full_name=file.filename,
                               supplier_id=supplier_id)
        db.session.add(db_file)
        db.session.flush()
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], db_file.internal_name))
        db_file.size = os.path.getsize(db_file.file_path)
        db.session.commit()


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
    def file_extension(self) -> str:
        """
        File's extension

        e.g. ``.pdf``, etc
        """
        return os.path.splitext(self.full_name)[1]

    @property
    def file_name(self) -> str:
        """
        File's base name

        e.g. ``hello`` of ``hello.pdf``
        """
        return os.path.splitext(self.full_name)[0]

    @property
    def internal_name(self) -> str:
        '''
        File's internal name

        Normally is ``id`` + ``extention``
        '''
        return f'{self.id}{self.file_extension}'

    @property
    def file_path(self) -> str:
        '''
        File's path in file system
        '''
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.internal_name)

    @property
    def size_humanized(self) -> str:
        '''
        Human readable file size

        e.g. ``4.1 kB``
        '''
        return naturalsize(self.size, format="%.2f")

    def delete(self):
        '''
        Move the file to the trash bin

        set the ``delete_date`` to current time, may be delete from the file system days later
        '''
        self.delete_date = datetime.utcnow()
        db.session.commit()

    def restore(self):
        '''
        Restore the file

        set the ``delete_date`` to ``None``
        '''
        self.delete_date = None
        db.session.commit()

    def update(self, form):
        '''
        Update file's information by the given form
        '''
        self.remark = form.remark.data
        self.full_name = form.file_name.data + self.file_extension
        db.session.commit()

    @staticmethod
    def split_ext(file: FileStorage) -> str:
        '''
        Get the extention of the given file
        '''
        return os.path.splitext(file.filename)[1]


class EmployeeFile(File):
    employee_id = Column(Integer, ForeignKey('employee.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'employee_file'
    }

    @property
    def owner_url(self) -> str:
        '''
        return url of the associated Employee's detail view
        '''
        return url_for('employee.detail', employee_id=self.employee_id, _anchor='Files')


class SupplierFile(File):
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'supplier_file'
    }

    @property
    def owner_url(self) -> str:
        '''
        return url of the associated Supplier's detail view
        '''
        return url_for('supplier.detail', supplier_id=self.supplier_id, _anchor='Files')
