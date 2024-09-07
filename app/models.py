from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Customer(Base):
    __tablename__ = 'Customers'

    id_customer = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
