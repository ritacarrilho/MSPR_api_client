from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    created_at: datetime
    name: str
    username: str
    first_name: str
    last_name: str
    postal_code: str
    city: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id_customer: int

    class Config:
        orm_mode = True

class CustomerUpdate(BaseModel):
    created_at: Optional[datetime] = None
    name: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None

    class Config:
        orm_mode = True