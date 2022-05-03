from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Summary(BaseModel):
    available: int
    categories: list
    
class TransactionBase(BaseModel):
    
    tdate: str
    outflow: int = 0
    inflow: int = 0
    payee: str    
    accountstr: str 
    categorystr: str = 'uncategorized'
    memo: Optional[str] = None
    cleared: bool = False
    reconciled: bool = False
    flagstr: Optional[str] = None

    class Config:
        orm_mode=True

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    pass
    # class Config:
    #     orm_mode=True

class Category(BaseModel):
    name: str
    section: str = 'none'
    order: int
    id: int

    class Config:
        orm_mode=True

class Section(BaseModel):
    name: str
    order: int

class Budgeted(BaseModel):
    assigned: int

    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode=True