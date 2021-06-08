import os

from citywok_ms import db
from citywok_ms.file.models import SupplierFile
from flask import current_app
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from werkzeug.datastructures import FileStorage


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


