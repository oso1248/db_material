from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, String, text, Numeric
from .. database.database import Base
from sqlalchemy.orm import relationship


class BridgeAddition(Base):
    __tablename__ = 'bridge_addition'

    id_brand_brewing = Column(Integer, ForeignKey('brand_brewing.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_commodity = Column(Integer, ForeignKey('commodity.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    per_brew = Column(Numeric(scale=2, precision=9), nullable=False)
    note = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    brand = relationship('BrandBrewing', foreign_keys=[id_brand_brewing])
    commodity = relationship('Commodity', foreign_keys=[id_commodity])


class BridgeKettleHop(Base):
    __tablename__ = 'bridge_kettle_hop'

    id_brand_brewing = Column(Integer, ForeignKey('brand_brewing.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_commodity = Column(Integer, ForeignKey('commodity.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    per_brew = Column(Numeric(scale=2, precision=9), nullable=False)
    note = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    brand = relationship('BrandBrewing', foreign_keys=[id_brand_brewing])
    commodity = relationship('Commodity', foreign_keys=[id_commodity])


class BridgeDryHop(Base):
    __tablename__ = 'bridge_dry_hop'

    id_brand_brewing = Column(Integer, ForeignKey('brand_brewing.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_commodity = Column(Integer, ForeignKey('commodity.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    per_brew = Column(Numeric(scale=2, precision=9), nullable=False)
    note = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    brand = relationship('BrandBrewing', foreign_keys=[id_brand_brewing])
    commodity = relationship('Commodity', foreign_keys=[id_commodity])
    