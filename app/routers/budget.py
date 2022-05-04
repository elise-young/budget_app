from fastapi import Body, FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, budgeter
from ..database import get_db

router = APIRouter(
    prefix="/budget",
    tags=['budget']
)

@router.put("/{id}", response_model=schemas.Budgeted)
def AssignBudget(id:int, newbudget: schemas.Budgeted, db: Session = Depends(get_db)):
    
    budget_query = db.query(models.Budgeted).filter(models.Budgeted.id == id)
    budget_item = budget_query.first()

    if budget_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category budget with id {id} does not exist")
    
    budget_query.update(newbudget.dict(), synchronize_session=False)
    db.commit()
    db.refresh(budget_item)
    return budget_query.first()
