from datetime import date
from operator import indexOf
from random import randrange
from re import I
from fastapi import Body, FastAPI, status, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

class Transaction(BaseModel):
    
    tdate: str
    outflow: int = 0
    inflow: int = 0
    payee: str
    accountid: int
    categoryid: int

transactions = []


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
    return {"data":transactions}

@app.post("/transactions", status_code=status.HTTP_201_CREATED)
def addTransaction(transaction: Transaction):
    my_transaction = transaction.dict()
    my_transaction['id'] = randrange(0,10000)
    transactions.append(my_transaction)
    return {"data":transactions}

@app.get("/transactions/{id}")
def getTransactionByID(id: int):
    thisTransaction = findTransaction(id)
    if not thisTransaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return {"data":thisTransaction}

@app.delete("/transactions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTransaction(id: int):

    index = findTransactionIndex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            defait=f"post with id {id} does not exist")
    transactions.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/transactions/{id}")
def updateTransaction(id : int, transaction : Transaction):
    index = findTransactionIndex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            defait=f"post with id {id} does not exist")
    transactionDict = transaction.dict()
    transactionDict['id'] = id
    transactions[index] = transactionDict
    return {"data": transactionDict}