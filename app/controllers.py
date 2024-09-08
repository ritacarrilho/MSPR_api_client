from sqlalchemy.orm import Session
from .models import Customer
# from .schemas import Customer as CustomerSchema

def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id_customer == customer_id).first()
