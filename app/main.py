"""
Module with all the API endpoints for clients management.
It includes the operations of creation, lecture, update and delete of clients
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends


app = FastAPI()

@app.get("/", response_model=dict, tags=["Health Check"])
def api_status():
    """
    Verifies the API status.

    Returns:
        dict: dict with the API status.
    """
    return {"status": "running"}



@app.get("/clients/", tags=["clients"])
def get_clients():
    return {"get clients": "ok"}


@app.get("/clients/{id}", tags=["clients"])
def get_clients():
    return {"get client by id": "ok"}