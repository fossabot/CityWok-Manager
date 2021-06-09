import citywok_ms.file.service as fileservice
import citywok_ms.supplier.service as supplierservice
from citywok_ms.file.forms import FileForm
from citywok_ms.supplier.forms import SupplierForm
from flask import Blueprint, flash, redirect, render_template, url_for

supplier = Blueprint("supplier", __name__, url_prefix="/supplier")


@supplier.route("/")
def index():
    return render_template(
        "supplier/index.html",
        title="Suppliers",
        suppliers=supplierservice.get_suppliers(),
    )


@supplier.route("/new", methods=["GET", "POST"])
def new():
    form = SupplierForm()
    if form.validate_on_submit():
        supplierservice.create_supplier(form)
        flash("Successfully added new supplier", "success")
        return redirect(url_for("supplier.index"))
    return render_template("supplier/form.html", title="New Supplier", form=form)


@supplier.route("/<int:supplier_id>")
def detail(supplier_id):
    return render_template(
        "supplier/detail.html",
        title="Supplier Detail",
        supplier=supplierservice.get_supplier(supplier_id),
        active_files=fileservice.get_supplier_active_files(supplier_id),
        deleted_files=fileservice.get_supplier_deleted_files(supplier_id),
        file_form=FileForm(),
    )


@supplier.route("/<int:supplier_id>/update", methods=["GET", "POST"])
def update(supplier_id):
    supplier = supplierservice.get_supplier(supplier_id)
    form = SupplierForm()
    form.hide_id.data = supplier_id
    if form.validate_on_submit():
        supplierservice.update_supplier(supplier, form)
        flash("Supplier information has been updated", "success")
        return redirect(url_for("supplier.detail", supplier_id=supplier_id))

    form.process(obj=supplier)

    return render_template(
        "supplier/form.html", supplier=supplier, form=form, title="Update supplier"
    )


@supplier.route("/<int:supplier_id>/upload", methods=["POST"])
def upload(supplier_id):
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        supplierservice.add_supplier_file(supplier_id, form)
        flash("File has been submited", "success")
    else:
        flash(f'Invalid File Format: "{fileservice.split_file_format(file)}"', "danger")
    return redirect(url_for("supplier.detail", supplier_id=supplier_id))
