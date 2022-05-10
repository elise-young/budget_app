from fastapi import Body, FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=['accounts']
)

#categories
@router.get("/", response_model=List[schemas.Account])
def getAccounts(db: Session = Depends(get_db)):
    
    accounts = db.query(models.Accounts).all()

    return accounts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Account)
def addAccount(account: schemas.AccountBase, db: Session = Depends(get_db)): 
     
    new_account = models.Accounts(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.put("/{id}", response_model=schemas.Account)
def updateAccount(id : int, updated_account : schemas.AccountUpdate, db: Session = Depends(get_db)):
    account_query = db.query(models.Accounts).filter(models.Accounts.id == id)
    account = account_query.first()

    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"account with id {id} does not exist")
    
    account_query.update(updated_account.dict(), synchronize_session=False)
    db.commit()
    db.refresh(account)
    return account_query.first()
