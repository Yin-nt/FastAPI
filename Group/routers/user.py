from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, schemas
from Group.core.validation import validate_email, validate_password
from Group.core import oauth2, hashing
from Group.crud import crud_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
get_db = database.get_db
# @router.post("/", response_model=schemas.ShowUser)
# def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email đã tồn tại!")
#     return crud_user.create_user(db=db, user=user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db, email=current_user.username)
    if not user:
        raise HTTPException(detail='Không tìm thấy người dùng!', status_code=status.HTTP_404_NOT_FOUND)
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
def read_user(db: Session = Depends(get_db),
              current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    db_user = crud_user.get_user_by_email(db, email=current_user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng!")
    return db_user


@router.post("/register", response_model=schemas.ShowUser)
def register_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    validate_email(user.email)
    validate_password(user.password)
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
    return crud_user.create_user(db=db, user=user)


@router.put("/update/{user_id}", response_model=schemas.ShowUser)
def update_user(updated_data: schemas.UpdateInfoUser, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    db_user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại.")
    return crud_user.Update_info_user(db=db, user_id=db_user.id, updated_data=updated_data)


@router.put("/change-password/{user_id}")
def change_password(new_data: schemas.ChangePassword,
                    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                    db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại.")
    if not hashing.Hash.verify(user.password, new_data.old_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không đúng.")
    validate_password(new_data.new_password)
    crud_user.change_password(db=db, user_id=user.id, new_password=new_data.new_password)
    return {"message": "Mật khẩu đã được thay đổi thành công, vui lòng đăng nhập lại."}
