from citywok_ms import db
from citywok_ms.models import Employee
from citywok_ms.employee.forms import EmployeeForm
from flask import Blueprint, flash, redirect, render_template, url_for


employee = Blueprint('employee', __name__, url_prefix="/employee")


@employee.route("/")
def index():
    employees = db.session.query(Employee).all()
    return render_template('employee/index.html', title='Employees', employees=employees)


@employee.route("/new", methods=['GET', 'POST'])
def new():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee()
        form.populate_obj(employee)
        db.session.add(employee)
        db.session.commit()
        flash('Successfully added new employee', 'success')
        return redirect(url_for('employee.index'))
    return render_template('employee/new.html', title='New Employee', form=form)


@employee.route("/<int:employee_id>")
def detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee/detail.html', title='Employee Detail', employee=employee)
