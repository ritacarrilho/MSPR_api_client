from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# --------------------- Customer Controllers --------------------- #

def get_customers(db: Session):
    """
    Récupère tous les clients.
    """
    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    """
    Récupère un client par ID.
    """
    return db.query(models.Customer).filter(models.Customer.id_customer == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    """
    Crée un nouveau client.
    """
    db_customer = models.Customer(
        name=customer.name,
        created_at=customer.created_at,
        username=customer.username,
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone=customer.phone,
        email=customer.email,
        password_hash=customer.password_hash,
        last_login=customer.last_login,
        customer_type=customer.customer_type,
        failed_login_attempts=customer.failed_login_attempts,
        preferred_contact_method=customer.preferred_contact_method,
        opt_in_marketing=customer.opt_in_marketing,
        loyalty_points=customer.loyalty_points
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerUpdate):
    """
    Met à jour les informations d'un client existant.
    """
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer_update.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    """
    Supprime un client par ID.
    """
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return None

    db.delete(db_customer)
    db.commit()
    return db_customer

# --------------------- Company Controllers --------------------- #

def get_all_companies(db: Session):
    """
    Récupère toutes les entreprises.
    """
    return db.query(models.Company).all()

def get_company_by_id(db: Session, company_id: int):
    """
    Récupère une entreprise par ID.
    """
    return db.query(models.Company).filter(models.Company.id_company == company_id).first()

def create_company(db: Session, company: schemas.CompanyCreate):
    """
    Crée une nouvelle entreprise.
    """
    db_company = models.Company(
        company_name=company.company_name,
        siret=company.siret,
        address=company.address,
        postal_code=company.postal_code,
        city=company.city,
        phone=company.phone,
        email=company.email
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_update: schemas.CompanyUpdate):
    """
    Met à jour une entreprise existante.
    """
    db_company = get_company_by_id(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company_update.dict(exclude_unset=True).items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    """
    Supprime une entreprise par ID.
    """
    db_company = get_company_by_id(db, company_id)
    if not db_company:
        return None

    db.delete(db_company)
    db.commit()
    return db_company

# --------------------- Feedback Controllers --------------------- #

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    """
    Crée un feedback pour un produit.
    """
    db_feedback = models.Customer_Feedback(
        product_id=feedback.product_id,
        rating=feedback.rating,
        comment=feedback.comment,
        created_at=feedback.created_at,
        id_customer=feedback.id_customer
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# --------------------- Notification Controllers --------------------- #

def create_notification(db: Session, notification: schemas.NotificationCreate):
    """
    Crée une notification pour un client.
    """
    db_notification = models.Notification(
        message=notification.message,
        date_created=notification.date_created,
        is_read=notification.is_read,
        type=notification.type,
        id_customer=notification.id_customer
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification