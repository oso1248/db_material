from sqlalchemy import Column, Integer, text, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from ..database.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    eid = Column(String, nullable=False, unique=True)
    name_first = Column(String, nullable=False)
    name_last = Column(String, nullable=False)
    password = Column(String, nullable=False)
    permissions = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by], remote_side=[id])
    updater = relationship('Users', foreign_keys=[updated_by], remote_side=[id])
    jobs = relationship("JobsBrewing", secondary="bridge_jobs_brewing",
                        primaryjoin="Users.id == BridgeJobsBrewing.id_user",
                        secondaryjoin="BridgeJobsBrewing.id_jobs_brewing == JobsBrewing.id",
                        backref='jobs_brewing',
                        viewonly=True)


class JobsBrewing(Base):
    __tablename__ = "jobs_brewing"

    id = Column(Integer, primary_key=True, nullable=False)
    name_job = Column(String(64), unique=True, nullable=False)
    name_area = Column(String(32), unique=False, nullable=False)
    job_order = Column(Integer, unique=False, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    note = Column(String(256), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    brewers = relationship("Users", secondary="bridge_jobs_brewing",
                        primaryjoin="JobsBrewing.id == BridgeJobsBrewing.id_jobs_brewing",
                        secondaryjoin="BridgeJobsBrewing.id_user == Users.id",
                        backref='users',
                        viewonly=True)


class BridgeJobsBrewing(Base):
    __tablename__ = "bridge_jobs_brewing"

    id_user = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_jobs_brewing = Column(Integer, ForeignKey('jobs_brewing.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    skap = Column(String(8), nullable=False)
    note = Column(Integer, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users", foreign_keys=[created_by])
    updater = relationship("Users", foreign_keys=[updated_by])
    brewer = relationship("Users", foreign_keys=[id_user])
    job = relationship("JobsBrewing", foreign_keys=[id_jobs_brewing])
