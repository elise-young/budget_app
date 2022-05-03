from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, Date, text
from sqlalchemy.sql.expression import null
from .database import Base

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    tdate = Column(Date, nullable=False)
    inflow = Column(Integer)
    outflow = Column(Integer)
    payee = Column(String)
    accountstr = Column(String)
    categorystr = Column(String)
    memo = Column(String)
    cleared = Column(Boolean, server_default='False')
    flagstr = Column(String)
    reconciled = Column(Boolean, server_default='False')

class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    section = Column(String)
    order = Column(Integer)

class Sections(Base):
    __tablename__ = "sections"
    name = Column(String, primary_key=True, nullable=False)
    order = Column(Integer)

class Budgeted(Base):
    __tablename__ = "budgeted"
    id = Column(Integer, primary_key=True, nullable=False)
    categoryid = Column(Integer)
    yearmonth = Column(Integer)
    assigned = Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))

