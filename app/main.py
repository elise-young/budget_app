from datetime import date, time
from operator import indexOf
from random import randrange
from re import I
from xmlrpc.client import boolean
from fastapi import Body, FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

class Transaction(BaseModel):
    
    tdate: str
    outflow: int = 0
    inflow: int = 0
    payee: str
    memo: Optional[str] = None
    accountstr: str 
    categorystr: str = 'uncategorized'
    cleared: bool = False
    reconciled: bool = False
    flagstr: Optional[str] = None


transactions = []

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


def findTransaction(id):
    for t in transactions:
        if t['id'] == id:
            return t

def findTransactionIndex(id):
    i=0
    while i < len(transactions):
        if transactions[i]['id'] == id:
            return i 
            break
        i+=1

@app.get("/")
async def root():
    return {"message!": "Hello World !!"}

@app.get("/transactions")
def getTransactions():
    cursor.execute("""SELECT * FROM transactions""")
    transactions = cursor.fetchall()
    print(transactions)
    return {"data":transactions}

@app.post("/transactions", status_code=status.HTTP_201_CREATED)
def addTransaction(transaction: Transaction):
    cursor.execute("""INSERT INTO transactions (tdate, payee, inflow, outflow, categorystr, accountstr, memo) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING * """,(
    transaction.tdate, transaction.payee, transaction.inflow, transaction.outflow, transaction.categorystr, transaction.accountstr, transaction.memo))    
    
    new_transaction = cursor.fetchone()
    conn.commit()    
    return {"data":new_transaction}

@app.get("/transactions/{id}")
def getTransactionByID(id: int):
    cursor.execute("""SELECT * FROM transactions WHERE id= %s """, (str(id)))
    thisTransaction = cursor.fetchone()
    if not thisTransaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return {"data":thisTransaction}

@app.delete("/transactions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTransaction(id: int):
    cursor.execute("""DELETE FROM transactions WHERE id = %s RETURNING *""", str(id))
    deletedTransaction = cursor.fetchone()
    conn.commit()
    if deletedTransaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            defait=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/transactions/{id}")
def updateTransaction(id : int, transaction : Transaction):
    cursor.execute("""UPDATE transactions SET tdate = %s, payee = %s, inflow = %s, outflow = %s, categorystr = %s, accountstr = %s, memo = %s WHERE id = %s RETURNING * """,(
    transaction.tdate, transaction.payee, transaction.inflow, transaction.outflow, transaction.categorystr, transaction.accountstr, transaction.memo, str(id)))    
    updatedTransaction = cursor.fetchone()
    conn.commit()
    if updatedTransaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            defait=f"post with id {id} does not exist")
    return {"data": updatedTransaction}