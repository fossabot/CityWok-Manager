from citywok_ms import db
from citywok_ms.employee.models import Employee, File
from citywok_ms.employee.forms import EmployeeForm
from citywok_ms.file.forms import FileForm
from flask import Blueprint, flash, redirect, render_template, url_for


employee = Blueprint('employee', __name__, url_prefix="/employee")


@employee.route("/")
def index():
    '''
    View which shows a resume of all employee
    '''
    employees = db.session.query(Employee).filter_by(active=True).all()
    i_employees = db.session.query(Employee).filter_by(active=False).all()
    return render_template('employee/index.html',
                           title='Employees',
                           employees=employees,
                           i_employees=i_employees)


@employee.route("/new", methods=['GET', 'POST'])
def new():
    '''
    View which creates a new Employee
    '''
    form = EmployeeForm()
    if form.validate_on_submit():
        Employee.new(form)
        flash('Successfully added new employee', 'success')
        return redirect(url_for('employee.index'))
    return render_template('employee/form.html',
                           title='New Employee',
                           form=form)


@employee.route("/<int:employee_id>")
def detail(employee_id):
    '''
    View which shows detail information of a Employee
    '''
    return render_template('employee/detail.html',
                           title='Employee Detail',
                           employee=Employee.query.get_or_404(employee_id),
                           file_form=FileForm())


@employee.route("/<int:employee_id>/update", methods=['GET', 'POST'])
def update(employee_id):
    '''
    View which updates information of a Employee
    '''
    employee = db.session.query(Employee).get_or_404(employee_id)
    form = EmployeeForm()
    form.hide_id.data = employee_id
    if form.validate_on_submit():
        employee.update(form)
        flash('Employee information has been updated', 'success')
        return redirect(url_for('employee.detail', employee_id=employee_id))

    form.process(obj=employee)

    return render_template('employee/form.html',
                           employee=employee,
                           form=form,
                           title='Update employee')


@employee.route("/<int:employee_id>/inactivate", methods=['POST'])
def inactivate(employee_id):
    '''
    View which inactivates a Employee
    '''
    employee = db.session.query(Employee).get_or_404(employee_id)
    employee.inactivate()
    flash('Employee has been inactivated', 'success')
    return redirect(url_for('employee.detail', employee_id=employee_id))


@employee.route("/<int:employee_id>/activate", methods=['POST'])
def activate(employee_id):
    '''
    View which activates a Employee
    '''
    employee = db.session.query(Employee).get_or_404(employee_id)
    employee.activate()
    flash('Employee has been activated', 'success')
    return redirect(url_for('employee.detail', employee_id=employee_id))


@employee.route("/<int:employee_id>/upload", methods=['POST'])
def upload(employee_id):
    '''
    View which uploads a file of a Employee
    '''
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        Employee.save_file(file=file, employee_id=employee_id)
        flash('File has been submited', 'success')
    else:
        flash(
            f'Invalid File Format: "{File.split_ext(file)}"', 'danger')
    return redirect(url_for('employee.detail', employee_id=employee_id))
