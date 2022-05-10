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
    accountid: int
    categoryid: Optional[int]
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



class CategoryUpdate(BaseModel):
    name: Optional[str]
    section: Optional[str] = 'none'
    order: Optional[int]

    class Config:
        orm_mode=True

class CategoryBase(BaseModel):
    name: str
    section: str = 'none'
    order: int

    class Config:
        orm_mode=True

class Category(CategoryBase):
    id: int



class AccountBase(BaseModel):
    name: str
    visible: bool = True
    group: str

    class Config:
        orm_mode=True

class Account(AccountBase):
    id: int

class AccountUpdate(BaseModel):
    name: Optional[str]
    visible: Optional[bool]
    group: Optional[bool]

class Section(BaseModel):
    name: str
    order: int

class Budgeted(BaseModel):
    assigned: int
    yearmonth: Optional[int]
    categoryid: Optional[int]

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