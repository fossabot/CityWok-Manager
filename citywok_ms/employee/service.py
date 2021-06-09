from citywok_ms.file.forms import FileForm
import os
from typing import List
from citywok_ms.file.models import EmployeeFile
from citywok_ms.employee.forms import EmployeeForm
from citywok_ms.employee.models import Employee
from citywok_ms import db
from flask import current_app


def create_employee(form: EmployeeForm):
    employee = Employee()
    form.populate_obj(employee)
    db.session.add(employee)
    db.session.commit()


def update_employee(employee: Employee, form: EmployeeForm):
    form.populate_obj(employee)
    db.session.commit()


def activate_employee(employee: Employee):
    employee.active = True
    db.session.commit()


def inactivate_employee(employee: Employee):
    employee.active = False
    db.session.commit()


def add_employee_file(employee_id: int, form: FileForm):
    file = form.file.data
    db_file = EmployeeFile(full_name=file.filename, employee_id=employee_id)
    db.session.add(db_file)
    db.session.flush()
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], db_file.internal_name))
    db_file.size = os.path.getsize(db_file.path)
    db.session.commit()


def get_all_employees() -> List[Employee]:
    return db.session.query(Employee).all()


def get_active_employees() -> List[Employee]:
    return db.session.query(Employee).filter_by(active=True).all()


def get_inactive_employees() -> List[Employee]:
    return db.session.query(Employee).filter_by(active=False).all()


def get_employee(employee_id: int) -> Employee:
    return db.session.query(Employee).get_or_404(employee_id)
