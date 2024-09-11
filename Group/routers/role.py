from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.crud import crud_role

router = APIRouter(
    tags = ["Roles"]
)
get_db = database.get_db

@router.post("/roles", response_model = schemas.ShowRole)
def create_role(role: schemas.CreateRole, db: Session = Depends(get_db)): #thiếu role
    return crud_role.create_role(db=db, role=role)
@router.get("/roles/{role_id}", response_model = schemas.ShowRole)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud_role.get_role(db, id=role_id)
    if not db_role:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Khong tim thay role.")
    return db_role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud_role.get_role(db, id=role_id)
    if not db_role:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Khong tim thay role.")
    db.delete(db_role)
    db.commit()
    return {"detail": "Role cua nguoi dung da duoc xoa."}
# @router.get("/user/{user_id}/roles", response_model =list[schemas.ShowRole])
# def read_all_role_of_user(
#         user_id: int, skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
#     roles = crud_role.get_role_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)
#     if not roles:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng.")
#     return roles