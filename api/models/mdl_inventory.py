from sqlalchemy import Column, Integer, text, String, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from ..database.database import Base


class InventoryUUID(Base):
    __tablename__ = "inventory_uuid"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text('gen_random_uuid()'))
    inventory_date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    child_material = relationship('InventoryMaterial',
                            backref='inventory_uuid',
                            primaryjoin='InventoryUUID.uuid == InventoryMaterial.uuid',
                            viewonly=True)
    child_hop = relationship('InventoryHop',
                            backref='inventory_uuid',
                            primaryjoin='InventoryUUID.uuid == InventoryHop.uuid',
                            viewonly=True)
    child_brews = relationship('InventoryLastBrews',
                            backref='inventory_uuid',
                            primaryjoin='InventoryUUID.uuid == InventoryLastBrews.uuid',
                            viewonly=True)
    child_hibernate = relationship('InventoryHibernate',
                               backref='inventory_uuid',
                               primaryjoin='InventoryUUID.uuid == InventoryHibernate.uuid',
                               viewonly=True)


class InventoryMaterial(Base):
    __tablename__ = "inventory_material"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), ForeignKey('inventory_uuid.uuid', ondelete='CASCADE'), nullable=False)
    id_commodity = Column(Integer, ForeignKey('commodity.id', ondelete='CASCADE'), nullable=False)
    final_count = Column(Numeric(scale=2, precision=9), nullable=False)
    final_total = Column(Numeric(scale=2, precision=9), nullable=False)
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    inventory = relationship("InventoryUUID", foreign_keys=[uuid])
    commodity = relationship("Commodity", foreign_keys=[id_commodity])


class InventoryLastBrews(Base):
    __tablename__ = "inventory_last_brews"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), ForeignKey('inventory_uuid.uuid', ondelete='CASCADE'), unique=True, nullable=False)
    bh_1 = Column(String(16), nullable=True)
    bh_2 = Column(String(16), nullable=True)
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    inventory = relationship("InventoryUUID", foreign_keys=[uuid])
    child = relationship('InventoryHop', backref='inventory_last_brews', primaryjoin='InventoryHop.uuid == foreign(InventoryLastBrews.uuid)', viewonly=True)


class InventoryHop(Base):
    __tablename__ = "inventory_hop"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), ForeignKey('inventory_uuid.uuid', ondelete='CASCADE'), ForeignKey('inventory_last_brews.uuid', ondelete='CASCADE'), nullable=False)
    id_commodity = Column(Integer, ForeignKey('commodity.id', ondelete='CASCADE'), nullable=False)
    final_boxes = Column(Numeric(scale=2, precision=9), nullable=False)
    final_pounds = Column(Numeric(scale=2, precision=9), nullable=False)
    final_total = Column(Numeric(scale=2, precision=9), nullable=False)
    lot_number = Column(String, nullable=False)
    is_current = Column(Boolean, nullable=False, server_default=text('False'))
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    inventory = relationship("InventoryUUID", foreign_keys=[uuid])
    last_brews = relationship('InventoryLastBrews', backref='inventory_hop', primaryjoin='foreign(InventoryHop.uuid) == InventoryLastBrews.uuid', viewonly=True)
    commodity = relationship("Commodity", foreign_keys=[id_commodity])


class InventoryHibernate(Base):
    __tablename__ = "inventory_hibernate"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), ForeignKey('inventory_uuid.uuid', ondelete='CASCADE'), nullable=False)
    id_brand_brewing = Column(Integer, ForeignKey('brand_brewing.id', ondelete='CASCADE'), nullable=False)
    tank_origin = Column(Integer, nullable=False)
    tank_origin_level = Column(Integer, nullable=False)
    tank_storage = Column(Integer, nullable=False)
    tank_storage_level = Column(Integer, nullable=False)
    tank_storage_og = Column(Numeric(scale=2, precision=9), nullable=False)
    tank_storage_abw = Column(Numeric(scale=2, precision=9), nullable=False)
    tank_storage_o2 = Column(Integer, nullable=True)
    note_origin = Column(String(256), nullable=True)
    tank_final = Column(Integer, nullable=True)
    tank_final_level = Column(Integer, nullable=True)
    note_final = Column(String(256), nullable=True)
    is_complete = Column(Boolean, nullable=False, server_default=text('False'))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    parent = relationship("InventoryUUID", foreign_keys=[uuid])
    brand = relationship("BrandBrewing", foreign_keys=[id_brand_brewing])
