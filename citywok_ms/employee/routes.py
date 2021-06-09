import citywok_ms.employee.service as employeeservice
import citywok_ms.file.service as fileservice
from citywok_ms.employee.forms import EmployeeForm
from citywok_ms.file.forms import FileForm
from flask import Blueprint, flash, redirect, render_template, url_for

employee = Blueprint("employee", __name__, url_prefix="/employee")


@employee.route("/")
def index():
    return render_template(
        "employee/index.html",
        title="Employees",
        employees=employeeservice.get_active_employees(),
        i_employees=employeeservice.get_inactive_employees(),
    )


@employee.route("/new", methods=["GET", "POST"])
def new():
    form = EmployeeForm()
    if form.validate_on_submit():
        employeeservice.create_employee(form)
        flash("Successfully added new employee", "success")
        return redirect(url_for("employee.index"))
    return render_template("employee/form.html", title="New Employee", form=form)


@employee.route("/<int:employee_id>")
def detail(employee_id):
    return render_template(
        "employee/detail.html",
        title="Employee Detail",
        employee=employeeservice.get_employee(employee_id),
        active_files=fileservice.get_employee_active_files(employee_id),
        deleted_files=fileservice.get_employee_deleted_files(employee_id),
        file_form=FileForm(),
    )


@employee.route("/<int:employee_id>/update", methods=["GET", "POST"])
def update(employee_id):
    employee = employeeservice.get_employee(employee_id)
    form = EmployeeForm()
    form.hide_id.data = employee_id
    if form.validate_on_submit():
        employeeservice.update_employee(employee, form)
        flash("Employee information has been updated", "success")
        return redirect(url_for("employee.detail", employee_id=employee_id))

    form.process(obj=employee)

    return render_template(
        "employee/form.html", employee=employee, form=form, title="Update employee"
    )


@employee.route("/<int:employee_id>/inactivate", methods=["POST"])
def inactivate(employee_id):
    employee = employeeservice.get_employee(employee_id)
    employeeservice.inactivate_employee(employee)
    flash("Employee has been inactivated", "success")
    return redirect(url_for("employee.detail", employee_id=employee_id))


@employee.route("/<int:employee_id>/activate", methods=["POST"])
def activate(employee_id):
    employee = employeeservice.get_employee(employee_id)
    employee.activate()
    flash("Employee has been activated", "success")
    return redirect(url_for("employee.detail", employee_id=employee_id))


@employee.route("/<int:employee_id>/upload", methods=["POST"])
def upload(employee_id):
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        employeeservice.add_employee_file(employee_id, form)
        flash("File has been submited", "success")
    else:
        flash(f'Invalid File Format: "{fileservice.split_file_format(file)}"', "danger")
    return redirect(url_for("employee.detail", employee_id=employee_id))
