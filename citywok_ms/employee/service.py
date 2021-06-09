from typing import List
from citywok_ms.employee.forms import EmployeeForm
from citywok_ms.employee.models import Employee
from citywok_ms import db


def create_employee(form: EmployeeForm) -> Employee:
    employee = Employee()
    form.populate_obj(employee)
    db.session.add(employee)
    db.session.commit()
    return employee


def update_employee(employee: Employee, form: EmployeeForm):
    form.populate_obj(employee)
    db.session.commit()


def activate_employee(employee: Employee):
    employee.active = True
    db.session.commit()


def inactivate_employee(employee: Employee):
    employee.active = False
    db.session.commit()


def get_all_employees() -> List[Employee]:
    return db.session.query(Employee).all()


def get_active_employees() -> List[Employee]:
    return db.session.query(Employee).filter_by(active=True).all()


def get_inactive_employees() -> List[Employee]:
    return db.session.query(Employee).filter_by(active=False).all()


def get_employee(employee_id: int) -> Employee:
    return db.session.query(Employee).get_or_404(employee_id)
