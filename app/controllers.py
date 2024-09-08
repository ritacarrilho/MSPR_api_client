from sqlalchemy.orm import Session
from .models import Customer
from .schemas import CustomerCreate

def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id_customer == customer_id).first()

def create_customer(db: Session, customer: CustomerCreate):
    """
    Crée un nouveau client dans la base de données.

    Args:
        db (Session): La session de base de données.
        customer (CustomerCreate): Les données du client à créer.

    Returns:
        Customer: Le client créé.
    """
    db_customer = Customer(
        created_at=customer.created_at,
        name=customer.name,
        username=customer.username,
        first_name=customer.first_name,
        last_name=customer.last_name,
        postal_code=customer.postal_code,
        city=customer.city
    )
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer