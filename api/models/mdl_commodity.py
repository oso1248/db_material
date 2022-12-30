from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text, Float
from sqlalchemy.orm import relationship
from .. database.database import Base


class Commodity(Base):
    __tablename__ = 'commodity'

    id = Column(Integer, primary_key=True, nullable=False)
    name_local = Column(String, unique=True, nullable=False)
    name_bit = Column(String, nullable=False)
    name_common = Column(String, nullable=False)
    inventory = Column(String, nullable=False)
    type = Column(String, nullable=False)
    sap = Column(String, nullable=False)
    unit_of_measurement = Column(String, nullable=False)
    per_unit = Column(Float, nullable=False)
    per_pallet = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    id_supplier = Column(Integer, ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    supplier = relationship('Suppliers', foreign_keys=[id_supplier])
