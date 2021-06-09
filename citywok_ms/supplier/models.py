from citywok_ms import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Supplier(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String)
    principal = Column(String)
    contact = Column(Integer)
    email = Column(String)
    nif = Column(Integer, unique=True)
    iban = Column(String, unique=True)
    address = Column(String)
    postcode = Column(String)
    city = Column(String)
    remark = Column(Text)

    files = relationship("File")

    def __repr__(self):
        return f"Supplier({self.id}: {self.name})"
