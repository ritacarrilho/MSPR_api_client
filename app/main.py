from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import controllers, schemas, models
from .database import get_db

app = FastAPI(
    title="Api Customer",
    description=".....",
    summary=".....",
    version="0.0.2",
)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/customers/", response_model=List[schemas.Customer], tags=["customers"])
def get_customers(db: Session = Depends(get_db)):
    customers = controllers.get_customers(db)
    return customers