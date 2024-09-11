from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, controllers
from .database import get_db
from typing import List

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Clients",
    version="0.0.2",
)

# @app.get("/test_db_connection/")
# def test_db_connection(db: Session = Depends(get_db)):
#     try:
#         # Juste pour tester la connexion
#         result = db.execute("SELECT 1")
#         return {"status": "success", "result": result.fetchone()}
#     except Exception as e:
#         return {"status": "error", "details": str(e)}

# ---------------------- Customer Endpoints ---------------------- #

@app.get("/customers/", response_model=List[schemas.Customer], tags=["Customers"])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère la liste des clients.
    """
    customers = controllers.get_customers(db)
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Récupère un client par ID.
    """
    customer = controllers.get_customer_by_id(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/", response_model=schemas.Customer, tags=["Customers"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau client.
    """
    return controllers.create_customer(db, customer)

@app.patch("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un client existant.
    """
    return controllers.update_customer(db, customer_id, customer_update)

@app.delete("/customers/{customer_id}", tags=["Customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Supprime un client par ID.
    """
    deleted_customer = controllers.delete_customer(db, customer_id)
    if deleted_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

# ---------------------- Company Endpoints ---------------------- #

@app.get("/companies/", response_model=List[schemas.Company], tags=["Companies"])
def read_companies(db: Session = Depends(get_db)):
    """
    Récupère la liste des entreprises.
    """
    companies = controllers.get_all_companies(db)
    return companies

@app.get("/companies/{company_id}", response_model=schemas.Company, tags=["Companies"])
def read_company(company_id: int, db: Session = Depends(get_db)):
    """
    Récupère une entreprise par ID.
    """
    company = controllers.get_company_by_id(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/companies/", response_model=schemas.Company, tags=["Companies"])
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle entreprise.
    """
    return controllers.create_company(db, company)

@app.patch("/companies/{company_id}", response_model=schemas.Company, tags=["Companies"])
def update_company(company_id: int, company_update: schemas.CompanyUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une entreprise existante.
    """
    return controllers.update_company(db, company_id, company_update)

@app.delete("/companies/{company_id}", tags=["Companies"])
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Supprime une entreprise par ID.
    """
    deleted_company = controllers.delete_company(db, company_id)
    if deleted_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}

# ---------------------- Feedback Endpoints ---------------------- #

@app.get("/feedbacks/", response_model=List[schemas.Feedback], tags=["Feedbacks"])
def read_feedbacks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère la liste des feedbacks.
    """
    feedbacks = controllers.get_feedbacks(db, skip=skip, limit=limit)
    return feedbacks

@app.get("/feedbacks/{feedback_id}", response_model=schemas.Feedback, tags=["Feedbacks"])
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Récupère un feedback par ID.
    """
    feedback = controllers.get_feedback_by_id(db, feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@app.post("/feedbacks/", response_model=schemas.Feedback, tags=["Feedbacks"])
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau feedback.
    """
    return controllers.create_feedback(db, feedback)

@app.patch("/feedbacks/{feedback_id}", response_model=schemas.Feedback, tags=["Feedbacks"])
def update_feedback(feedback_id: int, feedback_update: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un feedback existant.
    """
    return controllers.update_feedback(db, feedback_id, feedback_update)

@app.delete("/feedbacks/{feedback_id}", tags=["Feedbacks"])
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Supprime un feedback par ID.
    """
    deleted_feedback = controllers.delete_feedback(db, feedback_id)
    if deleted_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}

# ---------------------- Notification Endpoints ---------------------- #

@app.get("/notifications/", response_model=List[schemas.Notification], tags=["Notifications"])
def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère toutes les notifications.
    """
    return controllers.get_notifications(db, skip=skip, limit=limit)

@app.get("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    """
    Récupère une notification par ID.
    """
    notification = controllers.get_notification_by_id(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.post("/notifications/", response_model=schemas.Notification, tags=["Notifications"])
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    """
    Crée une notification pour un client.
    """
    return controllers.create_notification(db, notification)

@app.patch("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
def update_notification(notification_id: int, notification_update: schemas.NotificationUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une notification par ID.
    """
    notification = controllers.update_notification(db, notification_id, notification_update)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.delete("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """
    Supprime une notification par ID.
    """
    notification = controllers.delete_notification(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

# ---------------------- Address Endpoints ---------------------- #


@app.get("/addresses/", response_model=List[schemas.Address], tags=["Addresses"])
def get_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère toutes les adresses.
    """
    return controllers.get_addresses(db, skip=skip, limit=limit)

@app.post("/addresses/", response_model=schemas.Address, tags=["Addresses"])
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle adresse.
    """
    return controllers.create_address(db, address)

@app.get("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Récupère une adresse par ID.
    """
    address = controllers.get_address_by_id(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.patch("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def update_address(address_id: int, address_update: schemas.AddressUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une adresse par ID.
    """
    address = controllers.update_address(db, address_id, address_update)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.delete("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Supprime une adresse par ID.
    """
    address = controllers.delete_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address
