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

@app.post("/feedbacks/", response_model=schemas.FeedbackCreate, tags=["Feedbacks"])
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    """
    Crée un feedback pour un produit.
    """
    return controllers.create_feedback(db, feedback)

# ---------------------- Notification Endpoints ---------------------- #

@app.post("/notifications/", response_model=schemas.NotificationCreate, tags=["Notifications"])
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    """
    Crée une notification pour un client.
    """
    return controllers.create_notification(db, notification)