from typing import List

from citywok_ms import db
from citywok_ms.file.models import SupplierFile
from citywok_ms.supplier.forms import SupplierForm
from citywok_ms.supplier.models import Supplier


def create_supplier(form: SupplierForm) -> Supplier:
    supplier = Supplier()
    form.populate_obj(supplier)
    db.session.add(supplier)
    db.session.commit()
    return supplier


def update_supplier(supplier: Supplier, form: SupplierForm):
    form.populate_obj(supplier)
    db.session.commit()


def get_suppliers() -> List[Supplier]:
    return db.session.query(Supplier).all()


def get_supplier(supplier_id: int) -> Supplier:
    return db.session.query(Supplier).get_or_404(supplier_id)


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
