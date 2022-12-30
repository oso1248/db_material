from sqlalchemy import Column, Integer, text, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from ..database.database import Base


class BrandBrewing(Base):
    __tablename__ = "brand_brewing"

    id = Column(Integer, primary_key=True, nullable=False)
    name_brand = Column(String(4), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    is_organic = Column(Boolean, nullable=False, server_default=text('True'))
    is_dryhop = Column(Boolean, nullable=False, server_default=text('True'))
    is_addition = Column(Boolean, nullable=False, server_default=text('True'))
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    children = relationship('BrandFinishing',
                            backref='brand_brewing',
                            primaryjoin='BrandBrewing.id == BrandFinishing.id_brand_brewing',
                            viewonly=True)
    grandchildren = relationship("BrandPackaging", secondary="brand_finishing",
                                 primaryjoin="BrandBrewing.id == BrandFinishing.id_brand_brewing",
                                 secondaryjoin="BrandFinishing.id == BrandPackaging.id_brand_finishing",
                                 backref='brand_packaging',
                                 viewonly=True)


class BrandFinishing(Base):
    __tablename__ = "brand_finishing"

    id = Column(Integer, primary_key=True, nullable=False)
    id_brand_brewing = Column(Integer, ForeignKey('brand_brewing.id', ondelete='CASCADE'), nullable=False)
    name_brand = Column(String(4), unique=True, nullable=False)
    is_preinjection = Column(Boolean, nullable=False, server_default=text('True'))
    is_postinjection = Column(Boolean, nullable=False, server_default=text('True'))
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    parent = relationship('BrandBrewing', foreign_keys=[id_brand_brewing])
    children = relationship('BrandPackaging', backref='brand_finishing',
                            primaryjoin='BrandFinishing.id == BrandPackaging.id_brand_finishing',
                            viewonly=True)


class BrandPackaging(Base):
    __tablename__ = "brand_packaging"

    id = Column(Integer, primary_key=True, nullable=False)
    id_brand_finishing = Column(Integer, ForeignKey('brand_finishing.id', ondelete='CASCADE'), nullable=False)
    name_brand = Column(String(4), unique=True, nullable=False)
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    parent = relationship('BrandFinishing',
                          foreign_keys=[id_brand_finishing])
    grandparent = relationship("BrandBrewing", secondary="brand_finishing",
                               primaryjoin="BrandPackaging.id_brand_finishing == BrandFinishing.id",
                               secondaryjoin="BrandBrewing.id == BrandFinishing.id_brand_brewing",
                               viewonly=True)
