from sqlalchemy.orm import Session
from .models import Customer
from .schemas import CustomerCreate
from . import schemas

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

def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate):
    """
    Met à jour les données d'un client existant.

    Args:
        db (Session): La session de base de données.
        customer_id (int): L'ID du client à mettre à jour.
        customer_data (CustomerUpdate): Les nouvelles données du client.

    Returns:
        Customer: Le client mis à jour.
    """
    db_customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()

    if db_customer is None:
        raise NoResultFound("Customer not found")

    # Met à jour seulement les champs fournis
    update_data = customer_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer