from flask import Blueprint, flash, redirect, render_template, url_for
from citywok_ms.supplier.models import Supplier, File
from citywok_ms.supplier.forms import SupplierForm
from citywok_ms.file.forms import FileForm
from citywok_ms import db

supplier = Blueprint('supplier', __name__, url_prefix="/supplier")


@supplier.route("/")
def index():
    '''
    View to show a resumo of all suppliers
    '''
    suppliers = db.session.query(Supplier).all()
    return render_template('supplier/index.html',
                           title='Suppliers',
                           suppliers=suppliers)


@supplier.route("/new", methods=['GET', 'POST'])
def new():
    '''
    View to create a new supplier
    '''
    form = SupplierForm()
    if form.validate_on_submit():
        Supplier.new(form)
        flash('Successfully added new supplier', 'success')
        return redirect(url_for('supplier.index'))
    return render_template('supplier/form.html', title='New Supplier', form=form)


@supplier.route("/<int:supplier_id>")
def detail(supplier_id):
    '''
    View to show detail information of a supplier
    '''
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier/detail.html',
                           title='Supplier Detail',
                           supplier=supplier,
                           file_form=FileForm())


@supplier.route("/<int:supplier_id>/update", methods=['GET', 'POST'])
def update(supplier_id):
    '''
    View to update the information of a supplier
    '''
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm()
    form.hide_id.data = supplier_id
    if form.validate_on_submit():
        supplier.update(form)
        flash('Supplier information has been updated', 'success')
        return redirect(url_for('supplier.detail', supplier_id=supplier_id))

    form.process(obj=supplier)

    return render_template('supplier/form.html',
                           supplier=supplier,
                           form=form,
                           title='Update supplier')


@supplier.route("/<int:supplier_id>/upload", methods=['POST'])
def upload(supplier_id):
    '''
    View to upload a file of a supplier
    '''
    form = FileForm()
    file = form.file.data
    if form.validate_on_submit():
        Supplier.save_file(file=file, supplier_id=supplier_id)
        flash('File has been submited', 'success')
    else:
        flash(
            f'Invalid File Format: "{File.split_ext(file)}"', 'danger')
    return redirect(url_for('supplier.detail', supplier_id=supplier_id))
