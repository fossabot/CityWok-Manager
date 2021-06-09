from citywok_ms.file.models import SupplierFile
import os
from citywok_ms.file.forms import FileForm
from typing import List
from citywok_ms.supplier.models import Supplier
from citywok_ms.supplier.forms import SupplierForm
from citywok_ms import db
from flask import current_app


def create_supplier(form: SupplierForm):
    supplier = Supplier()
    form.populate_obj(supplier)
    db.session.add(supplier)
    db.session.commit()


def update_supplier(supplier: Supplier, form: SupplierForm):
    form.populate_obj(supplier)
    db.session.commit()


def get_suppliers() -> List[Supplier]:
    return db.session.query(Supplier).all()


def get_supplier(supplier_id: int) -> Supplier:
    return db.session.query(Supplier).get_or_404(supplier_id)


def add_supplier_file(supplier_id: int, form: FileForm):
    file = form.file.data
    db_file = SupplierFile(full_name=file.filename, supplier_id=supplier_id)
    db.session.add(db_file)
    db.session.flush()
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], db_file.internal_name))
    db_file.size = os.path.getsize(db_file.path)
    db.session.commit()


def get_supplier_active_files(supplier_id: int) -> List[SupplierFile]:
    return (
        db.session.query(SupplierFile)
        .filter(
            SupplierFile.supplier_id == supplier_id,
            SupplierFile.delete_date.is_(None),
        )
        .all()
    )


def get_supplier_deleted_files(supplier_id: int) -> List[SupplierFile]:
    return (
        db.session.query(SupplierFile)
        .filter(
            SupplierFile.supplier_id == supplier_id,
            SupplierFile.delete_date.isnot(None),
        )
        .all()
    )
