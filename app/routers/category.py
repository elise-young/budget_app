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
def addCategory(category: schemas.CategoryBase, db: Session = Depends(get_db)): 
     
    new_category = models.Categories(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.put("/{id}", response_model=schemas.Category)
def updateCategory(id : int, updated_category : schemas.CategoryUpdate, db: Session = Depends(get_db)):
    category_query = db.query(models.Categories).filter(models.Categories.id == id)
    category = category_query.first()

    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id {id} does not exist")
    
    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()
    db.refresh(category)
    return category_query.first()
