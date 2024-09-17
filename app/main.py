from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import threading
from . import models, schemas, controllers
from .database import get_db
from .messaging.service import fetch_customer_orders, fetch_order_products

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

# ---------------------- Customers Endpoints ---------------------- #

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

# ---------------------- Notifications Endpoints ---------------------- #

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

# ---------------------- Addresses Endpoints ---------------------- #

@app.get("/addresses/", response_model=List[schemas.Address], tags=["Addresses"])
def get_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère toutes les adresses.
    """
    return controllers.get_addresses(db, skip=skip, limit=limit)

@app.get("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Récupère une adresse par ID.
    """
    address = controllers.get_address_by_id(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.post("/addresses/", response_model=schemas.Address, tags=["Addresses"])
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle adresse.
    """
    return controllers.create_address(db, address)

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

# ---------------------- LoginLog Endpoints ---------------------- #

@app.get("/login-logs/", response_model=List[schemas.LoginLog], tags=["LoginLogs"])
def read_login_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return controllers.get_login_logs(db, skip=skip, limit=limit)

@app.get("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
def read_login_log(log_id: int, db: Session = Depends(get_db)):
    db_login_log = controllers.get_login_log_by_id(db, log_id)
    if db_login_log is None:
        raise HTTPException(status_code=404, detail="Login log not found")
    return db_login_log

@app.post("/login-logs/", response_model=schemas.LoginLog, tags=["LoginLogs"])
def create_login_log(login_log: schemas.LoginLogCreate, db: Session = Depends(get_db)):
    return controllers.create_login_log(db, login_log)

@app.patch("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
def update_login_log(log_id: int, login_log: schemas.LoginLogUpdate, db: Session = Depends(get_db)):
    db_login_log = controllers.update_login_log(db, log_id, login_log)
    if db_login_log is None:
        raise HTTPException(status_code=404, detail="Login log not found")
    return db_login_log

@app.delete("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
def delete_login_log(log_id: int, db: Session = Depends(get_db)):
    db_login_log = controllers.delete_login_log(db, log_id)
    if db_login_log is None:
        raise HTTPException(status_code=404, detail="Login log not found")
    return db_login_log

# ---------------------- CustomerCompany Endpoints ---------------------- #

@app.get("/customer-companies/", response_model=List[schemas.CustomerCompany], tags=["CustomerCompanies"])
def read_customer_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère toutes les relations entre clients et entreprises.
    """
    return controllers.get_customer_companies(db, skip=skip, limit=limit)

@app.get("/customer-companies/{customer_id}/{company_id}", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
def read_customer_company(customer_id: int, company_id: int, db: Session = Depends(get_db)):
    """
    Récupère une relation spécifique entre un client et une entreprise.
    """
    db_customer_company = controllers.get_customer_company_by_ids(db, customer_id, company_id)
    if db_customer_company is None:
        raise HTTPException(status_code=404, detail="CustomerCompany not found")
    return db_customer_company

@app.post("/customer-companies/", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
def create_customer_company(customer_company: schemas.CustomerCompanyCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle relation entre un client et une entreprise.
    """
    return controllers.create_customer_company(db, customer_company)

@app.patch("/customer-companies/{customer_id}/{company_id}", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
def update_customer_company(customer_id: int, company_id: int, customer_company_update: schemas.CustomerCompanyUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une relation existante entre un client et une entreprise.
    """
    return controllers.update_customer_company(db, customer_id, company_id, customer_company_update)

@app.delete("/customer-companies/{customer_id}/{company_id}", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
def delete_customer_company(customer_id: int, company_id: int, db: Session = Depends(get_db)):
    """
    Supprime une relation entre un client et une entreprise.
    """
    db_customer_company = controllers.delete_customer_company(db, customer_id, company_id)
    if db_customer_company is None:
        raise HTTPException(status_code=404, detail="CustomerCompany not found")
    return db_customer_company


@app.get("/customers/{customer_id}/orders", tags=["CustomerOrdersProducts"])
async def get_customer_orders(customer_id: int):
    """API endpoint to get a customer's orders."""
    try:
        orders = await fetch_customer_orders(customer_id)
        print(orders)
        if orders:
            return {"customer_id": customer_id, "orders": orders}
        else:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request to order service timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch customer orders: {str(e)}")
    

@app.get("/customers/{customer_id}/orders/{order_id}/products")
async def get_customer_order_products(customer_id: int, order_id: int):
    """Fetch products for a specific order of a customer."""
    try:
        products = await fetch_order_products(customer_id, order_id)
        print(f"Response products: {products}")
        if not products:
            raise HTTPException(status_code=404, detail="No products found for this order.")
        return {"customer_id": customer_id, "order_id": order_id, "products": products}
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products for order: {str(e)}")