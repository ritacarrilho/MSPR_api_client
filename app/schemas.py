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
    created_at: Optional[datetime]
    name: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    postal_code: Optional[str]
    city: Optional[str]

    class Config:
        orm_mode = True