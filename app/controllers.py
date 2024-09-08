from sqlalchemy.orm import Session
from .models import Customer
from .schemas import CustomerCreate
from . import models, schemas

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

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.id_customer == customer_id).first()

    if db_customer is None:
        return None

    db.delete(db_customer)
    db.commit()
    return db_customer

def get_all_companies(db: Session):
    return db.query(models.Company).all()

def get_company_by_id(db: Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id_company == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_data: schemas.CompanyUpdate):
    db_company = db.query(models.Company).filter(models.Company.id_company == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    update_data = company_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id_company == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(db_company)
    db.commit()

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id_order == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order_data: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id_order == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id_order == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()

def get_all_profiles(db: Session):
    return db.query(models.Profile).all()

def get_profile_by_id(db: Session, profile_id: int):
    profile = db.query(models.Profile).filter(models.Profile.id_profile == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile_data: schemas.ProfileUpdate):
    db_profile = db.query(models.Profile).filter(models.Profile.id_profile == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(models.Profile).filter(models.Profile.id_profile == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(db_profile)
    db.commit()