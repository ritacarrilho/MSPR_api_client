from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas, controllers
from .database import get_db
from typing import List
from .middleware import verify_password, create_access_token, get_current_customer, is_admin, is_customer_or_admin


# Initialisation de l'application FastAPI
app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Clients",
    version="0.0.2",
)

# ---------------------- Login Endpoints ---------------------- #
@app.post("/login")
async def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.email == login_data.email).first()

    if not customer or not verify_password(login_data.password, customer.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={
        "id_customer": customer.id_customer,
        "email": customer.email,
        "customer_type": customer.customer_type 
    })

    print(f"Login successful. Generated token payload: customer_type={customer.customer_type}")
    
    return {"access_token": access_token, "token_type": "bearer"}


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
async def read_customers(db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère la liste des clients.
    """
    is_admin(current_customer)
    try:
        customers = controllers.get_customers(db)
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching customers")


@app.get("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
async def read_customer(customer_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère un client par ID.
    """
    is_customer_or_admin(current_customer, customer_id)
    try:
        customer = controllers.get_customer_by_id(db, customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the customer")


@app.post("/customers/", response_model=schemas.Customer, tags=["Customers"])
async def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau client.
    """
    try:
        new_customer = controllers.create_customer(db, customer)
        return new_customer
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the customer")


@app.patch("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
async def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour un client existant.
    """
    is_customer_or_admin(current_customer, customer_id)
    try:
        updated_customer = controllers.update_customer(db, customer_id, customer_update)
        if updated_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the customer")


@app.delete("/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime un client par ID.
    """
    is_customer_or_admin(current_customer, customer_id)
    try:
        deleted_customer = controllers.delete_customer(db, customer_id)
        if deleted_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"message": f"Customer with id {customer_id} was successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the customer")


# ---------------------- Company Endpoints ---------------------- #

@app.get("/companies/", response_model=List[schemas.Company], tags=["Companies"])
async def read_companies(db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère la liste des entreprises.
    """
    is_admin(current_customer)
    
    try:
        companies = controllers.get_all_companies(db)
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the companies")


@app.get("/companies/{company_id}", response_model=schemas.Company, tags=["Companies"])
async def read_company(company_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère une entreprise par ID.
    """
    try:
        if is_customer_or_admin(current_customer, current_customer["id_customer"]): 
            company = controllers.get_company_by_id(db, company_id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")
            return company
        
        # customer_company = controllers.get_customer_company_by_ids(db, current_customer["id_customer"], company_id)
        # if not customer_company:
        #     raise HTTPException(status_code=403, detail="You are not authorized to access this company")
        
        company = controllers.get_company_by_id(db, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return company

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the company")


@app.post("/companies/", response_model=schemas.Company, tags=["Companies"])
async def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée une nouvelle entreprise.
    """
    try:
        if is_customer_or_admin(current_customer, current_customer["id_customer"]):
            new_company = controllers.create_company(db, company)
        if not new_company:
            raise HTTPException(status_code=400, detail="Company could not be created")
        
        return new_company

    except HTTPException:
        raise 
    except Exception as e:
        print(f"Error creating company: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the company")


@app.patch("/companies/{company_id}", response_model=schemas.Company, tags=["Companies"])
async def update_company(company_id: int, company_update: schemas.CompanyUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour une entreprise existante.
    """
    try:
        if is_customer_or_admin(current_customer, current_customer["id_customer"]):
            customer_company = controllers.get_customer_company_by_ids(db, current_customer["id_customer"], company_id)
            if not customer_company:
                raise HTTPException(status_code=403, detail="You are not authorized to update this company")

        updated_company = controllers.update_company(db, company_id, company_update)
        if not updated_company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return updated_company

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating company: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the company")


@app.delete("/companies/{company_id}", tags=["Companies"])
async def delete_company(company_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime une entreprise par ID.
    """
    try:
        if is_customer_or_admin(current_customer, current_customer["id_customer"]):
            customer_company = controllers.get_customer_company_by_ids(db, current_customer["id_customer"], company_id)
            if not customer_company:
                raise HTTPException(status_code=403, detail="You are not authorized to delete this company")
        
        deleted_company = controllers.delete_company(db, company_id)
        if not deleted_company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {"message": f"Company with id {company_id} was successfully deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the company")


# ---------------------- Feedback Endpoints ---------------------- #

@app.get("/feedbacks/", response_model=List[schemas.Feedback], tags=["Feedbacks"])
async def read_feedbacks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère la liste des feedbacks.
    """
    try:
        is_admin(current_customer)
        feedbacks = controllers.get_feedbacks(db, skip=skip, limit=limit)
        
        if not feedbacks:
            raise HTTPException(status_code=404, detail="No feedbacks found")
        
        return feedbacks
    
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving feedbacks")


@app.get("/feedbacks/{feedback_id}", response_model=schemas.Feedback, tags=["Feedbacks"])
async def read_feedback(feedback_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère un feedback par ID.
    """
    try:
        feedback = controllers.get_feedback_by_id(db, feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        if feedback.id_customer != current_customer["id_customer"] and current_customer["customer_type"] != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this feedback")
        
        return feedback

    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving feedback")


@app.post("/feedbacks/", response_model=schemas.Feedback, tags=["Feedbacks"])
async def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée un nouveau feedback.
    """
    try:
        if not current_customer or "id_customer" not in current_customer:
            raise HTTPException(status_code=401, detail="You must be authenticated to create feedback.")
        
        feedback.id_customer = current_customer["id_customer"]
        created_feedback = controllers.create_feedback(db, feedback)
        return created_feedback
    
    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error creating feedback: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the feedback")
    

@app.patch("/feedbacks/{feedback_id}", response_model=schemas.Feedback, tags=["Feedbacks"])
async def update_feedback(feedback_id: int, feedback_update: schemas.FeedbackUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour un feedback existant.
    """
    try:
        feedback = controllers.get_feedback_by_id(db, feedback_id)
        
        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

        if feedback.id_customer != current_customer["id_customer"] and current_customer["customer_type"] != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this feedback")

        updated_feedback =  controllers.update_feedback(db, feedback_id, feedback_update)
        return updated_feedback
    
    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error updating feedback: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the feedback")


@app.delete("/feedbacks/{feedback_id}", tags=["Feedbacks"])
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime un feedback par ID.
    """
    try:
        feedback = controllers.get_feedback_by_id(db, feedback_id)

        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

        if feedback.id_customer != current_customer["id_customer"] and current_customer["customer_type"] != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this feedback")

        controllers.delete_feedback(db, feedback_id)
        return {"detail": f"Feedback with ID {feedback_id} has been successfully deleted"}

    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error deleting feedback: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the feedback")


# ---------------------- Notifications Endpoints ---------------------- #

@app.get("/notifications/", response_model=List[schemas.Notification], tags=["Notifications"])
async def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère toutes les notifications.
    """
    try:
        is_admin(current_customer)
        notifications = controllers.get_notifications(db, skip=skip, limit=limit)

        if not notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")

        return notifications

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving notifications: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving notifications")


@app.get("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
async def read_notification(notification_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère une notification par ID.
    """
    try:
        notification = controllers.get_notification_by_id(db, notification_id)

        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

        if notification.id_customer != current_customer["id_customer"] and current_customer["customer_type"] != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this notification")

        return notification

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving notification: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the notification")


@app.post("/notifications/", response_model=schemas.Notification, tags=["Notifications"])
async def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée une notification pour un client.
    """
    try:
        if not current_customer:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to create a notification")

        new_notification = controllers.create_notification(db, notification)
        return new_notification

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating notification: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the notification")


@app.patch("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
async def update_notification(notification_id: int, notification_update: schemas.NotificationUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour une notification par ID.
    """
    try:
        notification = controllers.get_notification_by_id(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        is_admin(current_customer)
        updated_notification = controllers.update_notification(db, notification_id, notification_update)
        return updated_notification

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error updating notification: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the notification")


@app.delete("/notifications/{notification_id}", response_model=schemas.Notification, tags=["Notifications"])
async def delete_notification(notification_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime une notification par ID.
    """
    try:
        notification = controllers.get_notification_by_id(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        is_admin(current_customer)
        controllers.delete_notification(db, notification_id)
        return {"message": f"Company with id {notification_id} was successfully deleted"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error deleting notification: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the notification")


# ---------------------- Addresses Endpoints ---------------------- #

@app.get("/addresses/", response_model=List[schemas.Address], tags=["Addresses"])
async def get_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère toutes les adresses.
    """
    try:
        is_admin(current_customer)
        addresses = controllers.get_addresses(db, skip=skip, limit=limit)

        if not addresses:
            raise HTTPException(status_code=404, detail="No addresses found")
        return addresses

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving addresses: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving addresses")
    

@app.get("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
async def get_address(address_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère une adresse par ID.
    """
    try:
        address = controllers.get_address_by_id(db, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if current_customer["customer_type"] != 1 and address.id_customer != current_customer["id_customer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this address"
            )
        return address

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error retrieving address with id {address_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the address")


@app.post("/addresses/", response_model=schemas.Address, tags=["Addresses"])
async def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée une nouvelle adresse.
    """
    try:
        if not current_customer or "id_customer" not in current_customer:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be logged in to create an address"
            )
    
        address.id_customer = current_customer["id_customer"]
        new_address = controllers.create_address(db, address)
        
        return new_address

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating address: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the address")


@app.patch("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
async def update_address(address_id: int, address_update: schemas.AddressUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour une adresse par ID.
    """
    try:
        address = controllers.get_address_by_id(db, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if current_customer["customer_type"] != 1 and address.id_customer != current_customer["id_customer"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this address")

        updated_address = controllers.update_address(db, address_id, address_update)
        return updated_address

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error updating address: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the address")


@app.delete("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
async def delete_address(address_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime une adresse par ID.
    """
    try:
        address = controllers.get_address_by_id(db, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if current_customer["customer_type"] != 1 and address.id_customer != current_customer["id_customer"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this address")

        controllers.delete_address(db, address_id)
        return {"detail": f"Address with id {address_id} was successfully deleted"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error deleting address: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the address")


# ---------------------- LoginLog Endpoints ---------------------- #

@app.get("/login-logs/", response_model=List[schemas.LoginLog], tags=["LoginLogs"])
async def read_login_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère les login logs.
    """
    try:
        is_admin(current_customer)
        login_logs = controllers.get_login_logs(db, skip=skip, limit=limit)

        if not login_logs:
            raise HTTPException(status_code=404, detail="No login logs found")

        return login_logs
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving login logs: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving login logs")


@app.get("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
async def read_login_log(log_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère les login log par ID.
    """
    try:
        log = controllers.get_login_log_by_id(db, log_id)
        
        if not log:
            raise HTTPException(status_code=404, detail="Login log not found")
        
        is_customer_or_admin(current_customer, log.id_customer)
        return log
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving login log: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the login log")


@app.post("/login-logs/", response_model=schemas.LoginLog, tags=["LoginLogs"])
async def create_login_log(login_log: schemas.LoginLogCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée un nouveau login log.
    """
    try:
        is_admin(current_customer)
        new_log = controllers.create_login_log(db, login_log)
        return new_log

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating login log: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the login log")


@app.patch("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
async def update_login_log(log_id: int, login_log: schemas.LoginLogUpdate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Met à jour un login log par ID.
    """
    try:
        log = controllers.get_login_log_by_id(db, log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Login log not found")
        
        is_admin(current_customer)
        updated_log = controllers.update_login_log(db, log_id, login_log)
        return updated_log

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        print(f"Error updating login log: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the login log")
    

@app.delete("/login-logs/{log_id}", response_model=schemas.LoginLog, tags=["LoginLogs"])
async def delete_login_log(log_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime un login log par ID.
    """
    try:
        log = controllers.get_login_log_by_id(db, log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Login log not found")

        is_admin(current_customer)
        controllers.delete_login_log(db, log_id)
        return {"message": f"Login log with id {log_id} was successfully deleted"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting login log: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the login log")


# ---------------------- CustomerCompany Endpoints ---------------------- #

@app.get("/customer-companies/", response_model=List[schemas.CustomerCompany], tags=["CustomerCompanies"])
async def read_customer_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère toutes les relations entre clients et entreprises.
    """
    try:
        is_admin(current_customer)
        customer_companies = controllers.get_customer_companies(db, skip=skip, limit=limit)

        if not customer_companies:
            raise HTTPException(status_code=404, detail="No customer-company relationships found")
        
        return customer_companies

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving customer-companies: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving customer-company relationships")


@app.get("/customer-companies/{customer_id}/{company_id}", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
async def read_customer_company(customer_id: int, company_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Récupère une relation spécifique entre un client et une entreprise.
    """
    try:
        is_admin(current_customer)
        customer_company = controllers.get_customer_company_by_ids(db, customer_id, company_id)

        if not customer_company:
            raise HTTPException(status_code=404, detail="CustomerCompany relationship not found")
        return customer_company

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving customer-company relationship: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the customer-company relationship")


@app.post("/customer-companies/", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
async def create_customer_company(customer_company: schemas.CustomerCompanyCreate, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Crée une nouvelle relation entre un client et une entreprise.
    """
    try:
        is_admin(current_customer)
        new_customer_company = controllers.create_customer_company(db, customer_company)
        return new_customer_company

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error creating customer-company relationship: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the customer-company relationship")


@app.delete("/customer-companies/{customer_id}/{company_id}", response_model=schemas.CustomerCompany, tags=["CustomerCompanies"])
async def delete_customer_company(customer_id: int, company_id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_customer)):
    """
    Supprime une relation entre un client et une entreprise.
    """
    try:
        is_customer_or_admin(current_customer, customer_id)
        customer_company = controllers.get_customer_company_by_ids(db, customer_id, company_id)
        if not customer_company:
            raise HTTPException(status_code=404, detail="CustomerCompany not found")

        controllers.delete_customer_company(db, customer_id, company_id)
        return {"detail": f"Company with id {company_id} belonging to {customer_id} was successfully deleted"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error deleting customer-company relationship: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the customer-company relationship")
    