# main.py
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import get_db
from . import controllers, schemas

app = FastAPI(
    title="Api Customer",
    description=".....",
    summary=".....",
    version="0.0.2",
)

@app.get("/", response_model=dict, tags=["Health Check"])
def api_status():
    """
    Verifies the API status.

    Returns:
        dict: dict with the API status.
    """
    return {"status": "running :)"}

@app.get("/customers/", response_model=List[schemas.Customer], tags=["customers"])
def get_customers(db: Session = Depends(get_db)):
    """
    Get all customers from the database.

    Returns:
        List[schemas.Customer]: List of all customers.
    """
    customers = controllers.get_customers(db)
    return customers

@app.get("/customers/{id}", response_model=schemas.Customer, tags=["customers"])
def get_customer(id: int, db: Session = Depends(get_db)):
    """
    Get a customer by their ID.

    Args:
        id (int): Customer ID.
        db (Session): Database session.

    Returns:
        schemas.Customer: Customer data.
    """
    customer = controllers.get_customer_by_id(db, id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer