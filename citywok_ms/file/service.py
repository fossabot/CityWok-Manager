from datetime import datetime
from citywok_ms.file.forms import FileForm, FileUpdateForm
import os
from typing import List
from flask import current_app

from werkzeug.datastructures import FileStorage

from citywok_ms import db
from citywok_ms.file.models import EmployeeFile, File, SupplierFile


def get_file(file_id: int) -> File:
    return db.session.query(File).get_or_404(file_id)


def delete_file(file: File):
    file.delete_date = datetime.utcnow()
    db.session.commit()


def restore_file(file: File):
    file.delete_date = None
    db.session.commit()


def update_file(file: File, form: FileUpdateForm):
    file.remark = form.remark.data
    file.base_name = form.file_name.data
    db.session.commit()


def split_file_format(file: FileStorage) -> str:
    return os.path.splitext(file.filename)[1]


def get_employee_active_files(employee_id: int) -> List[EmployeeFile]:
    return (
        db.session.query(EmployeeFile)
        .filter(
            EmployeeFile.employee_id == employee_id,
            EmployeeFile.delete_date.is_(None),
        )
        .all()
    )


def get_employee_deleted_files(employee_id: int) -> List[EmployeeFile]:
    return (
        db.session.query(EmployeeFile)
        .filter(
            EmployeeFile.employee_id == employee_id,
            EmployeeFile.delete_date.isnot(None),
        )
        .all()
    )


def get_supplier_active_files(supplier_id: int) -> List[SupplierFile]:
    return (
        db.session.query(SupplierFile)
        .filter(
            SupplierFile.supplier_id == supplier_id,
            SupplierFile.delete_date.is_(None),
        )
        .all()
    )


def get_supplier_deleted_files(supplier_id: int) -> List[SupplierFile]:
    return (
        db.session.query(SupplierFile)
        .filter(
            SupplierFile.supplier_id == supplier_id,
            SupplierFile.delete_date.isnot(None),
        )
        .all()
    )


def add_employee_file(employee_id: int, form: FileForm) -> EmployeeFile:
    file = form.file.data
    db_file = EmployeeFile(full_name=file.filename, employee_id=employee_id)
    db.session.add(db_file)
    db.session.flush()
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], db_file.internal_name))
    db_file.size = os.path.getsize(db_file.path)
    db.session.commit()
    return db_file


def add_supplier_file(supplier_id: int, form: FileForm) -> SupplierFile:
    file = form.file.data
    db_file = SupplierFile(full_name=file.filename, supplier_id=supplier_id)
    db.session.add(db_file)
    db.session.flush()
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], db_file.internal_name))
    db_file.size = os.path.getsize(db_file.path)
    db.session.commit()
    return db_file
