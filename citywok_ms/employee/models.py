import os

from citywok_ms import db
from citywok_ms.file.models import EmployeeFile
from citywok_ms.utils import ID, SEX
from citywok_ms.utils.models import SqliteDecimal
from flask import current_app
from sqlalchemy import Boolean, Column, Date, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates
from sqlalchemy_utils import ChoiceType, CountryType
from werkzeug.datastructures import FileStorage


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
