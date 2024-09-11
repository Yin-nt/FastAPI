from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.core.validation import validate_email, validate_password
from Group.core import oauth2
from Group.crud import crud_user

router = APIRouter(
    prefix="/users",
    tags=["User"]
)
get_db = database.get_db
@router.post("/", response_model=schemas.ShowUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
    return crud_user.create_user(db=db, user=user)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db, email=current_user.username)
    if not user:
        raise HTTPException(detail='Không tìm thấy người dùng!',status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
    return {'detail': 'Người dùng đã được xóa!'}
# @router.put("/{user_id}", status_code= status.HTTP_202_ACCEPTED)
# def update(user_id: int , request: schemas.CreateUser, db: Session = Depends(get_db)):
#     pass

# @router.get("/", response_model=list[schemas.ShowUser])
# def read_users(current_user: schemas.TokenData = Depends(oauth2.get_current_user),
#         skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud_user.get_users(db, skip=skip, limit=limit)
#     return users


@router.get("/{user_id}", response_model=schemas.ShowUser)
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    db_user = crud_user.get_user_by_email(db, email=current_user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng!")
    return db_user

@router.post("/new", response_model=schemas.ShowUser)
def register_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    validate_email(user.email)
    validate_password(user.password)
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
    return crud_user.create_user(db=db, user=user)
