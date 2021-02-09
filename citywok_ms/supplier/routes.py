from flask import Blueprint, flash, redirect, render_template, url_for
from citywok_ms.models import Supplier, SupplierFile, File
from citywok_ms.supplier.forms import SupplierForm
from citywok_ms.file.forms import FileForm
from citywok_ms import db

supplier = Blueprint('supplier', __name__, url_prefix="/supplier")


@supplier.route("/")
def index():
    suppliers = db.session.query(Supplier).all()
    return render_template('supplier/index.html',
                           title='Suppliers',
                           suppliers=suppliers)


@supplier.route("/new", methods=['GET', 'POST'])
def new():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier()
        form.populate_obj(supplier)
        db.session.add(supplier)
        db.session.commit()
        flash('Successfully added new supplier', 'success')
        return redirect(url_for('supplier.index'))
    return render_template('supplier/new.html', title='New Supplier', form=form)


@supplier.route("/<int:supplier_id>")
def detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier/detail.html',
                           title='Supplier Detail',
                           supplier=supplier,
                           file_form=FileForm())


@supplier.route("/<int:supplier_id>/update", methods=['GET', 'POST'])
def update(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm()
    form.hide_id.data = supplier_id
    if form.validate_on_submit():
        form.populate_obj(supplier)
        db.session.commit()
        flash('Supplier information has been updated', 'success')
        return redirect(url_for('supplier.detail', supplier_id=supplier_id))

    form.process(obj=supplier)

    return render_template('supplier/update.html',
                           supplier=supplier,
                           form=form,
                           title='Update supplier')


@supplier.route("/<int:supplier_id>/upload", methods=['POST'])
def upload(supplier_id):
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        SupplierFile.save_file(file=file, supplier_id=supplier_id)
        flash('File has been submited', 'success')
    else:
        flash(
            f'Invalid File Format: "{File.split_ext(file)}"', 'danger')
    return redirect(url_for('supplier.detail', supplier_id=supplier_id))
