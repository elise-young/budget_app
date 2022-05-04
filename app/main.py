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
from .routers import transaction, category, budget, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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


app.include_router(transaction.router)
app.include_router(category.router)
app.include_router(budget.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message!": "Hello World !!"}

@app.get("/summary", response_model=schemas.Summary)
def getTransactions(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM transactions""")
    # transactions = cursor.fetchall()

    summary = budgeter.GetSummary()

    return summary






