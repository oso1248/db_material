from .. database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text
from sqlalchemy.orm import relationship


class Suppliers(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, nullable=False)
    name_supplier = Column(String, unique=True, nullable=False)
    name_contact = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    note = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    # children = relationship('Commodities', backref='suppliers', primaryjoin='Suppliers.id == Commodities.id_supplier', viewonly=True)
