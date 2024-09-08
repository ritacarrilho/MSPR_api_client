from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, controllers
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

@app.get("/test_db_connection/")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Juste pour tester la connexion
        result = db.execute("SELECT 1")
        return {"status": "success", "result": result.fetchone()}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/customers/", response_model=List[schemas.Customer], tags=["customers"])
def get_customers(db: Session = Depends(get_db)):
    customers = controllers.get_customers(db)
    return customers


