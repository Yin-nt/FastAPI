from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sql_app import database, crud, models, schemas
from sql_app.routers import item

router = APIRouter(
    # tags='Users'
)
get_db = database.get_db
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() # first() returns the first  that match the
    # condition
    if not user:
        raise HTTPException(detail='User not found',status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
    return {'detail': 'User deleted'}
@router.put("/users/{user_id}", status_code= status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, df: Session = Depends(get_db)):
    pass
@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.ShowUsers) # only show email and item
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
