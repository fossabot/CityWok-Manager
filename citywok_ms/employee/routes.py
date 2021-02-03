from citywok_ms import db
from citywok_ms.models import Employee
from citywok_ms.employee.forms import EmployeeForm
from flask import Blueprint, flash, redirect, render_template, url_for


employee = Blueprint('employee', __name__, url_prefix="/employee")


@employee.route("/")
def index():
    employees = db.session.query(Employee).filter_by(active=True).all()
    i_employees = db.session.query(Employee).filter_by(active=False).all()
    return render_template('employee/index.html',
                           title='Employees',
                           employees=employees,
                           i_employees=i_employees)


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


@employee.route("/<int:employee_id>/update", methods=['GET', 'POST'])
def update(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm()
    form.hide_id.data = employee_id
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Employee information has been updated', 'success')
        return redirect(url_for('employee.detail', employee_id=employee_id))

    form.process(obj=employee)

    return render_template('employee/update.html',
                           employee=employee,
                           form=form,
                           title='Update employee')


@employee.route("/<int:employee_id>/inactivate", methods=['POST'])
def inactivate(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.active = False
    db.session.commit()
    flash('Employee has been inactivated', 'success')
    return redirect(url_for('employee.detail', employee_id=employee_id))


@employee.route("/<int:employee_id>/activate", methods=['POST'])
def activate(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.active = True
    db.session.commit()
    flash('Employee has been activated', 'success')
    return redirect(url_for('employee.detail', employee_id=employee_id))
