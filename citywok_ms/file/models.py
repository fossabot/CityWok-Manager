import os
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from citywok_ms import db
from flask import current_app, url_for
from humanize import naturalsize
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text


class File(db.Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    delete_date = Column(DateTime)
    size = Column(Integer)
    remark = Column(Text)

    type = Column(String)

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "file"}

    def __repr__(self):
        return f"File({self.id}: {self.full_name})"

    @property
    def formate(self) -> str:
        return os.path.splitext(self.full_name)[1]

    @hybrid_property
    def base_name(self) -> str:
        return os.path.splitext(self.full_name)[0]

    @base_name.setter
    def base_name(self, new_name: str):
        self.full_name = new_name + self.formate

    @property
    def internal_name(self) -> str:
        return f"{self.id}{self.formate}"

    @property
    def path(self) -> str:
        return os.path.join(current_app.config["UPLOAD_FOLDER"], self.internal_name)

    @property
    def humanized_size(self) -> str:
        return naturalsize(self.size, format="%.2f")


class EmployeeFile(File):
    employee_id = Column(Integer, ForeignKey("employee.id"))

    __mapper_args__ = {"polymorphic_identity": "employee_file"}

    @property
    def owner_url(self) -> str:
        return url_for("employee.detail", employee_id=self.employee_id, _anchor="Files")


class SupplierFile(File):
    supplier_id = Column(Integer, ForeignKey("supplier.id"))

    __mapper_args__ = {"polymorphic_identity": "supplier_file"}

    @property
    def owner_url(self) -> str:
        return url_for("supplier.detail", supplier_id=self.supplier_id, _anchor="Files")
