from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from .middleware import hash_password

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
    Create a new customer with a hashed password.
    """
    # Hash the password before saving it
    hashed_password = hash_password(customer.password_hash)  # Use the plain password and hash it

    db_customer = models.Customer(
        name=customer.name,
        created_at=customer.created_at,
        username=customer.username,
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone=customer.phone,
        email=customer.email,
        password_hash=hashed_password,  # Store the hashed password
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

def get_feedbacks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Feedback).offset(skip).limit(limit).all()

def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(models.Feedback).filter(models.Feedback.id_feedback == feedback_id).first()

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: int, feedback_update: schemas.FeedbackUpdate):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id_feedback == feedback_id).first()
    if db_feedback:
        for key, value in feedback_update.dict(exclude_unset=True).items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id_feedback == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback

# --------------------- Notification Controllers --------------------- #

def get_notifications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Notification).offset(skip).limit(limit).all()

def get_notification_by_id(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.id_notification == notification_id).first()

def create_notification(db: Session, notification: schemas.NotificationCreate):
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

def update_notification(db: Session, notification_id: int, notification_update: schemas.NotificationUpdate):
    db_notification = db.query(models.Notification).filter(models.Notification.id_notification == notification_id).first()
    if db_notification:
        for key, value in notification_update.dict(exclude_unset=True).items():
            setattr(db_notification, key, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int):
    db_notification = db.query(models.Notification).filter(models.Notification.id_notification == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification

# --------------------- Address Controllers --------------------- #

def get_addresses(db: Session, skip: int = 0, limit: int = 10):
    """
    Récupère toutes les adresses.
    """
    return db.query(models.Address).offset(skip).limit(limit).all()

def get_address_by_id(db: Session, address_id: int):
    """
    Récupère une adresse par ID.
    """
    return db.query(models.Address).filter(models.Address.id_address == address_id).first()

def create_address(db: Session, address: schemas.AddressCreate):
    """
    Crée une nouvelle adresse.
    """
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address_update: schemas.AddressUpdate):
    """
    Met à jour une adresse existante.
    """
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in address_update.dict(exclude_unset=True).items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    """
    Supprime une adresse par ID.
    """
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return None

    db.delete(db_address)
    db.commit()
    return db_address

# --------------------- LoginLog Controllers --------------------- #

def get_login_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LoginLog).offset(skip).limit(limit).all()

def get_login_log_by_id(db: Session, log_id: int):
    return db.query(models.LoginLog).filter(models.LoginLog.id_log == log_id).first()

def create_login_log(db: Session, login_log: schemas.LoginLogCreate):
    db_login_log = models.LoginLog(**login_log.dict())
    db.add(db_login_log)
    db.commit()
    db.refresh(db_login_log)
    return db_login_log

def update_login_log(db: Session, log_id: int, login_log_update: schemas.LoginLogUpdate):
    db_login_log = db.query(models.LoginLog).filter(models.LoginLog.id_log == log_id).first()
    if not db_login_log:
        raise HTTPException(status_code=404, detail="Login log not found")

    for key, value in login_log_update.dict(exclude_unset=True).items():
        setattr(db_login_log, key, value)

    db.commit()
    db.refresh(db_login_log)
    return db_login_log

def delete_login_log(db: Session, log_id: int):
    db_login_log = db.query(models.LoginLog).filter(models.LoginLog.id_log == log_id).first()
    if not db_login_log:
        return None

    db.delete(db_login_log)
    db.commit()
    return db_login_log

# --------------------- CustomerCompany Controllers --------------------- #

def get_customer_companies(db: Session, skip: int = 0, limit: int = 10):
    """
    Récupère toutes les relations entre clients et entreprises.
    """
    return db.query(models.CustomerCompany).offset(skip).limit(limit).all()

def get_customer_company_by_ids(db: Session, customer_id: int, company_id: int):
    """
    Récupère une relation spécifique entre un client et une entreprise.
    """
    return db.query(models.CustomerCompany).filter(
        models.CustomerCompany.id_customer == customer_id,
        models.CustomerCompany.id_company == company_id
    ).first()

def create_customer_company(db: Session, customer_company: schemas.CustomerCompanyCreate):
    """
    Crée une nouvelle relation entre un client et une entreprise.
    """
    # Vérifier si la relation existe déjà
    existing_relation = db.query(models.CustomerCompany).filter(
        models.CustomerCompany.id_customer == customer_company.id_customer,
        models.CustomerCompany.id_company == customer_company.id_company
    ).first()
    
    if existing_relation:
        raise HTTPException(status_code=400, detail="CustomerCompany relation already exists")

    db_customer_company = models.CustomerCompany(
        id_customer=customer_company.id_customer,
        id_company=customer_company.id_company
    )
    db.add(db_customer_company)
    db.commit()
    db.refresh(db_customer_company)
    return db_customer_company

def update_customer_company(db: Session, customer_id: int, company_id: int, customer_company_update: schemas.CustomerCompanyUpdate):
    """
    Met à jour une relation existante entre un client et une entreprise.
    """
    db_customer_company = db.query(models.CustomerCompany).filter(
        models.CustomerCompany.id_customer == customer_id,
        models.CustomerCompany.id_company == company_id
    ).first()
    
    if not db_customer_company:
        raise HTTPException(status_code=404, detail="CustomerCompany not found")

    # Update foreign keys if needed
    db_customer_company.id_customer = customer_company_update.id_customer
    db_customer_company.id_company = customer_company_update.id_company

    db.commit()
    db.refresh(db_customer_company)
    return db_customer_company

def delete_customer_company(db: Session, customer_id: int, company_id: int):
    """
    Supprime une relation entre un client et une entreprise.
    """
    db_customer_company = db.query(models.CustomerCompany).filter(
        models.CustomerCompany.id_customer == customer_id,
        models.CustomerCompany.id_company == company_id
    ).first()
    
    if not db_customer_company:
        return None

    db.delete(db_customer_company)
    db.commit()
    return db_customer_company