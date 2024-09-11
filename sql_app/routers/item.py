from typing import List
from fastapi import APIRouter, Depends
from sql_app import schemas, database, crud, models, oauth
from sqlalchemy.orm import Session

# from sql_app.database import SessionLocal
router = APIRouter(
    prefix='/items',
    tags=['Items']
)

@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth.get_current_user)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(database.get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)