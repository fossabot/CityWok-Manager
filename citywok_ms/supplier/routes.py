import citywok_ms.file.message as filemsg
import citywok_ms.file.service as fileservice
import citywok_ms.supplier.message as suppliermsg
import citywok_ms.supplier.service as supplierservice
from citywok_ms.file.forms import FileForm
from citywok_ms.supplier.forms import SupplierForm
from flask import Blueprint, flash, redirect, render_template, url_for

supplier = Blueprint("supplier", __name__, url_prefix="/supplier")


@supplier.route("/")
def index():
    return render_template(
        "supplier/index.html",
        title=suppliermsg.INDEX_TITLE,
        suppliers=supplierservice.get_suppliers(),
    )


@supplier.route("/new", methods=["GET", "POST"])
def new():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = supplierservice.create_supplier(form)
        flash(suppliermsg.UPDATE_SUCCESS.format(name=supplier.name), "success")
        return redirect(url_for("supplier.index"))
    return render_template("supplier/form.html", title=suppliermsg.NEW_TITLE, form=form)


@supplier.route("/<int:supplier_id>")
def detail(supplier_id):
    return render_template(
        "supplier/detail.html",
        title=suppliermsg.INDEX_TITLE,
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
        flash(suppliermsg.UPDATE_SUCCESS.format(name=supplier.name), "success")
        return redirect(url_for("supplier.detail", supplier_id=supplier_id))

    form.process(obj=supplier)

    return render_template(
        "supplier/form.html",
        supplier=supplier,
        form=form,
        title=suppliermsg.UPDATE_TITLE,
    )


@supplier.route("/<int:supplier_id>/upload", methods=["POST"])
def upload(supplier_id):
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        db_file = fileservice.add_supplier_file(supplier_id, form)
        flash(filemsg.UPLOAD_SUCCESS.format(name=db_file.full_name), "success")
    else:
        flash(
            filemsg.INVALID_FORMAT.format(format=fileservice.split_file_format(file)),
            "danger",
        )
    return redirect(url_for("supplier.detail", supplier_id=supplier_id))
