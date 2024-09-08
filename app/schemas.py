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
        
class CompanyBase(BaseModel):
    company_name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id_customer: int
    id_company: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    created_at: datetime

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id_customer: int
    id_order: int

    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    first_name: str
    last_name: str

class ProfileCreate(ProfileBase):
    id_customer: int

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id_profile: int

    class Config:
        orm_mode = True