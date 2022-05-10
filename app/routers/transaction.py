from fastapi import Body, FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=['transactions']
)

#transactions
@router.get("/", response_model=List[schemas.Transaction])
def getTransactions(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions""")
    # transactions = cursor.fetchall()

    transactions = db.query(models.Transactions).all()

    return transactions

@router.get("/{id}", response_model=schemas.Transaction)
def getTransactionByID(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions WHERE id= %s """, (str(id)))
    # transaction = cursor.fetchone()
    
    transaction = db.query(models.Transactions).filter(models.Transactions.id == id).first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"transaction with id {id} does not exist")
    
    return transaction

@router.get("/{accountid}", response_model=List[schemas.Transaction])
def getTransactionsByAccount(accountid: int, db: Session = Depends(get_db)):

    transactions = db.query(models.Transactions).filter(models.Transactions.accountid == accountid).all()

    return transactions

@router.get("/{categoryid}", response_model=List[schemas.Transaction])
def getTransactionsByCategory(categoryid: int, db: Session = Depends(get_db)):

    transactions = db.query(models.Transactions).filter(models.Transactions.categoryid == categoryid).all()

    return transactions

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionCreate)
def addTransaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO transactions (tdate, payee, inflow, outflow, categorystr, accountstr, memo) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING * """,(
    # transaction.tdate, transaction.payee, transaction.inflow, transaction.outflow, transaction.categorystr, transaction.accountstr, transaction.memo))    
    # new_transaction = cursor.fetchone()
    # conn.commit()   
     
    new_transaction = models.Transactions(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTransaction(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM transactions WHERE id = %s RETURNING *""", str(id))
    # deleted_transaction = cursor.fetchone()
    # conn.commit()

    deleted_transaction = db.query(models.Transactions).filter(models.Transactions.id == id)
    
    if deleted_transaction.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"transaction with id {id} does not exist")
    
    deleted_transaction.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.TransactionCreate)
def updateTransaction(id : int, updated_transaction : schemas.TransactionCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE transactions SET tdate = %s, payee = %s, inflow = %s, outflow = %s, categorystr = %s, accountstr = %s, memo = %s WHERE id = %s RETURNING * """,(
    # transaction.tdate, transaction.payee, transaction.inflow, transaction.outflow, transaction.categorystr, transaction.accountstr, transaction.memo, str(id)))    
    # updatedTransaction = cursor.fetchone()
    # conn.commit()

    transaction_query = db.query(models.Transactions).filter(models.Transactions.id == id)
    transaction = transaction_query.first()

    if transaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"transaction with id {id} does not exist")
    
    transaction_query.update(updated_transaction.dict(), synchronize_session=False)
    db.commit()
    db.refresh(transaction)
    return transaction_query.first()