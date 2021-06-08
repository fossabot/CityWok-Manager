import os
from datetime import datetime

from citywok_ms import db
from flask import current_app, url_for
from humanize import naturalsize
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from werkzeug.datastructures import FileStorage


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
