from typing import List

from citywok_ms import db
from citywok_ms.file.models import SupplierFile


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
