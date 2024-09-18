from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schéma de base pour Customer
class CustomerBase(BaseModel):
    created_at: datetime
    name: str
    username: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: str
    last_login: datetime
    customer_type: int
    failed_login_attempts: Optional[int] = 0
    preferred_contact_method: Optional[int] = None
    opt_in_marketing: Optional[bool] = False
    loyalty_points: Optional[int] = 0
    role: str

# Schéma pour la création d'un Customer
class CustomerCreate(CustomerBase):
    password_hash: str
    role: Optional[str] = "customer"
    

# Schéma pour le retour d'un Customer
class Customer(CustomerBase):
    id_customer: int

    class Config:
        orm_mode = True

# Schéma pour la mise à jour d'un Customer
class CustomerUpdate(BaseModel):
    created_at: Optional[datetime] = None
    name: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    last_login: Optional[datetime] = None
    customer_type: Optional[int] = None
    failed_login_attempts: Optional[int] = None
    preferred_contact_method: Optional[int] = None
    opt_in_marketing: Optional[bool] = None
    loyalty_points: Optional[int] = None

    class Config:
        orm_mode = True

# Schéma de base pour Company
class CompanyBase(BaseModel):
    company_name: str
    siret: str
    address: str
    postal_code: str
    city: str
    phone: Optional[str] = None
    email: Optional[str] = None

# Schéma pour la création d'une Company
class CompanyCreate(CompanyBase):
    pass

# Schéma pour la mise à jour d'une Company
class CompanyUpdate(CompanyBase):
    pass

# Schéma pour le retour d'une Company
class Company(CompanyBase):
    id_company: int

    class Config:
        orm_mode = True

# Schéma de base pour Feedback
class FeedbackBase(BaseModel):
    product_id: int
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: datetime

# Schéma pour le retour d'un Feedback
class Feedback(FeedbackBase):
    id_feedback: int
    id_customer: int

    class Config:
        orm_mode = True

# Schéma pour la création d'un Feedback
class FeedbackBase(BaseModel):
    product_id: int
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    id_customer: int

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Feedback(FeedbackBase):
    id_feedback: int

    class Config:
        orm_mode = True

# Schéma pour Notification
class NotificationBase(BaseModel):
    message: str
    date_created: Optional[datetime] = None
    is_read: Optional[bool] = False
    type: int
    id_customer: int

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    message: Optional[str] = None
    date_created: Optional[datetime] = None
    is_read: Optional[bool] = None
    type: Optional[int] = None
    id_customer: Optional[int] = None

class Notification(NotificationBase):
    id_notification: int

    class Config:
        orm_mode = True

class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    address_type: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    id_customer: int

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    address_type: Optional[int] = None
    updated_at: Optional[datetime] = None

class Address(AddressBase):
    id_address: int

    class Config:
        orm_mode = True


class LoginLogBase(BaseModel):
    login_time: datetime
    ip_address: str = None
    user_agent: str = None
    id_customer: int

class LoginLogCreate(LoginLogBase):
    pass

class LoginLogUpdate(BaseModel):
    login_time: datetime = None
    ip_address: str = None
    user_agent: str = None

class LoginLog(LoginLogBase):
    id_log: int

    class Config:
        orm_mode = True


# Schéma pour Login
class LoginRequest(BaseModel):
    email: str
    password: str

#

class CustomerCompanyBase(BaseModel):
    id_customer: int
    id_company: int

class CustomerCompanyCreate(CustomerCompanyBase):
    pass

class CustomerCompanyUpdate(BaseModel):
    id_customer: int
    id_company: int

    class Config:
        orm_mode = True

class CustomerCompany(CustomerCompanyBase):
    class Config:
        orm_mode = True
