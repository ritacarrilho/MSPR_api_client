from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = 'customers'

    id_customer = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)

class Company(Base):
    __tablename__ = "companies"

    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), primary_key=True)
    id_company = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(80), nullable=False)

    customer = relationship("Customer", back_populates="companies")

class Order(Base):
    __tablename__ = "orders"

    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), primary_key=True)
    id_order = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)

    customer = relationship("Customer", back_populates="orders")

class Profile(Base):
    __tablename__ = "profiles"

    id_profile = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(50), nullable=False)
    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), nullable=False)

    customer = relationship("Customer", back_populates="profiles")

# Ajoute les relations inverses dans le modèle Customer
class Customer(Base):
    __tablename__ = "Customers"

    id_customer = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String(80), nullable=False)
    username = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(90), nullable=False)

    companies = relationship("Company", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    profiles = relationship("Profile", back_populates="customer", cascade="all, delete-orphan")