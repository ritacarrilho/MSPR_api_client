from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "Customers"

    id_customer = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    username = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    phone = Column(String(15))
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime, nullable=False)
    customer_type = Column(Integer, nullable=False)
    failed_login_attempts = Column(Integer, default=0)
    preferred_contact_method = Column(Integer)
    opt_in_marketing = Column(Boolean)
    loyalty_points = Column(Integer, nullable=False, default=0)

    companies = relationship("Company", secondary="Customer_Companies")
    feedbacks = relationship("Feedback", back_populates="customer")
    notifications = relationship("Notification", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")
    login_logs = relationship("LoginLog", back_populates="customer")

class Company(Base):
    __tablename__ = "Companies"

    id_company = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(80), nullable=False)
    siret = Column(String(15), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(90), nullable=False)
    phone = Column(String(15))
    email = Column(String(100), unique=True)

    customers = relationship("Customer", secondary="Customer_Companies")

class Feedback(Base):
    __tablename__ = "Customer_Feedback"

    id_feedback = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    rating = Column(Integer)
    comment = Column(String(50))
    created_at = Column(DateTime)
    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), nullable=False)

    customer = relationship("Customer", back_populates="feedbacks")

class Notification(Base):
    __tablename__ = "Notifications"

    id_notification = Column(Integer, primary_key=True, index=True)
    message = Column(String(255), nullable=False)
    date_created = Column(DateTime)
    is_read = Column(Boolean, default=False)
    type = Column(Integer, nullable=False)
    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), nullable=False)

    customer = relationship("Customer", back_populates="notifications")

class Address(Base):
    __tablename__ = "Addresses"

    id_address = Column(Integer, primary_key=True, index=True)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    address_type = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), nullable=False)

    customer = relationship("Customer", back_populates="addresses")

class LoginLog(Base):
    __tablename__ = "Login_Logs"

    id_log = Column(Integer, primary_key=True, index=True)
    login_time = Column(DateTime, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), nullable=False)

    customer = relationship("Customer", back_populates="login_logs")

class CustomerCompany(Base):
    __tablename__ = "Customer_Companies"

    id_customer = Column(Integer, ForeignKey("Customers.id_customer"), primary_key=True)
    id_company = Column(Integer, ForeignKey("Companies.id_company"), primary_key=True)
    
    customer = relationship("Customer", backref="customer_companies")
    company = relationship("Company", backref="company_customers")