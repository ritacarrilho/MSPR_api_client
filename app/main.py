from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, controllers
from .database import get_db

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

@app.get("/customers/", response_model=List[schemas.Customer], tags=["customers"])
def get_customers(db: Session = Depends(get_db)):
    """
    Récupère tous les clients de la base de données.

    Args:
        db (Session): La session de base de données.

    Returns:
        List[schemas.Customer]: Liste de tous les clients.
    """
    customers = controllers.get_customers(db)
    return customers

@app.get("/customers/{id}", response_model=schemas.Customer, tags=["customers"])
def get_customer(id: int, db: Session = Depends(get_db)):
    """
     Récupère un client par son ID.

    Args:
        id (int): L'ID du client.
        db (Session): La session de base de données.

    Returns:
        schemas.Customer: Les données du client.

    Raises:
        HTTPException: Si le client avec l'ID spécifié n'est pas trouvé.
    """
    customer = controllers.get_customer_by_id(db, id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/", response_model=schemas.Customer, tags=["customers"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau client dans la base de données.

    Args:
        customer (schemas.CustomerCreate): Les données du client à créer.
        db (Session): La session de base de données.

    Returns:
        schemas.Customer: Les données du client créé.
    """
    db_customer = controllers.create_customer(db, customer)
    return db_customer

@app.patch("/customers/{id}", response_model=schemas.Customer, tags=["customers"])
def update_customer(id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un client existant avec les données fournies.

    Args:
        id (int): L'ID du client à mettre à jour.
        customer (schemas.CustomerUpdate): Les données à modifier.
        db (Session): La session de base de données.

    Returns:
        schemas.Customer: Les données mises à jour du client.
    """
    db_customer = controllers.update_customer(db, id, customer)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{id}", response_model=schemas.Customer, tags=["customers"])
def delete_customer(id: int, db: Session = Depends(get_db)):
    """
    Supprime un client par son ID.

    Args:
        id (int): L'ID du client à supprimer.
        db (Session): La session de base de données.

    Returns:
        schemas.Customer: Les données du client supprimé, ou une erreur 404 s'il n'est pas trouvé.
    """
    db_customer = controllers.delete_customer(db, id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer