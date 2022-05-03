from datetime import date, time
from typing import Optional, List
from operator import indexOf
from re import I
from xmlrpc.client import boolean
from fastapi import Body, FastAPI, status, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from . import models, schemas, utils, budgeter
from .database import engine, get_db
from datetime import date
import requests


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='mybudget', user='eliseyoung', 
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print('connection error')
        print('Error:', error)
        time.sleep(5)


@app.get("/")
async def root():
    return {"message!": "Hello World !!"}

@app.get("/summary", response_model=schemas.Summary)
def getTransactions(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions""")
    # transactions = cursor.fetchall()

    summary = budgeter.GetSummary()

    return summary

@app.put("/budget/{id}", response_model=schemas.Budgeted)
def MonthChange(id:int, newbudget: schemas.Budgeted, db: Session = Depends(get_db)):
    
    budget_query = db.query(models.Budgeted).filter(models.Budgeted.id == id)
    budget_item = budget_query.first()

    if budget_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category budget with id {id} does not exist")
    
    budget_query.update(newbudget.dict(), synchronize_session=False)
    db.commit()
    db.refresh(budget_item)
    return budget_query.first()


#transactions
@app.get("/transactions", response_model=List[schemas.Transaction])
def getTransactions(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions""")
    # transactions = cursor.fetchall()

    transactions = db.query(models.Transactions).all()

    return transactions


@app.post("/transactions", status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionCreate)
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

@app.get("/transactions/{id}", response_model=schemas.Transaction)
def getTransactionByID(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions WHERE id= %s """, (str(id)))
    # transaction = cursor.fetchone()
    
    transaction = db.query(models.Transactions).filter(models.Transactions.id == id).first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"transaction with id {id} does not exist")
    
    return transaction

@app.delete("/transactions/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.put("/transactions/{id}", response_model=schemas.TransactionCreate)
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

#categories
@app.get("/categories", response_model=List[schemas.Category])
def getCategories(db: Session = Depends(get_db)):
    
    categories = db.query(models.Categories).all()

    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED, response_model=schemas.Category)
def addCategory(category: schemas.Category, db: Session = Depends(get_db)): 
     
    new_category = models.Categories(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

#users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user