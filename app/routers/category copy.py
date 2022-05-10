from fastapi import Body, FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=['categories']
)

#categories
@router.get("/", response_model=List[schemas.Category])
def getCategories(db: Session = Depends(get_db)):
    
    categories = db.query(models.Categories).all()

    return categories


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Category)
def addCategory(category: schemas.Category, db: Session = Depends(get_db)): 
     
    new_category = models.Categories(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category
