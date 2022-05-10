from fastapi import Body, FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils, budgeter
from ..database import get_db

router = APIRouter(
    prefix="/budget",
    tags=['budget']
)

@router.get("/{yearmonth}", response_model=List[schemas.Budgeted])
def GetBudgetByMonth(yearmonth:int, db: Session = Depends(get_db)):
    
    budget_query = db.query(models.Budgeted).filter(models.Budgeted.yearmonth == yearmonth).all()

    
    return budget_query


@router.put("/{categoryid}/{yearmonth}", status_code=status.HTTP_201_CREATED, response_model=schemas.Budgeted)
def AssignBudget(categoryid:int, yearmonth:int, newbudget: schemas.Budgeted, db: Session = Depends(get_db)):
    
    category_query = db.query(models.Categories).filter(models.Categories.id == categoryid)
    category_item = category_query.first()
    budget_query = db.query(models.Budgeted).filter(models.Budgeted.categoryid == categoryid, models.Budgeted.yearmonth == yearmonth)
    budget_item = budget_query.first()

    if category_item == None:
        

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category budget for {categoryid} and {yearmonth} does not exist")
    elif budget_item == None:
        budget_item = models.Budgeted(**newbudget.dict())
        budget_item.categoryid = categoryid
        budget_item.yearmonth = yearmonth
        db.add(budget_item)
        db.commit()
        db.refresh(budget_item)
    else:
        budget_query.update(newbudget.dict(), synchronize_session=False)
        db.commit()
        db.refresh(budget_item)
    return budget_query.first()


