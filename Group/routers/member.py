from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.crud import crud_member, crud_user
from Group.core import oauth2
router = APIRouter(
    tags=["Members"]
)
get_db = database.get_db
@router.post("/members", response_model=schemas.ShowMember)
def create_member(member: schemas.CreateMember, db: Session = Depends(get_db)):
    db_member = crud_member.get_member_by_user_and_group_id(db, user_id=member.user_id, group_id=member.group_id)
    if db_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User đã tồn tại trong group.")
    return crud_member.create_member(db=db, member=member)
# @router.get("/members/{member_id}", response_model = schemas.ShowMember)
# def read_member(member_id: int, db: Session = Depends(get_db),
#                 current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
#     db_member = db.query(models.Group_member).filter(models.Group_member.id == member_id).first()
#     if not db_member:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thành viên.")
#     return db_member
@router.get("/group/{group_id}/members", response_model =list[schemas.ShowMember])
def read_all_member_of_group(
        group_id: int, skip: int = 0, limit: int = 100,
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),):
    members = crud_member.get_all_members(db=db, group_id=group_id, skip=skip, limit=limit)
    if not members:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thành viên nào.")
    return members
@router.delete("/groups/{group_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
        group_id: int, member_id: int,
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=current_user.username)
    if not crud_member.is_admin(db, user.id, group_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xóa thành viên.")
    db_member = db.query(models.Group_member).filter(
        models.Group_member.user_id == member_id,#user trong group
        models.Group_member.group_id == group_id
    ).first()
    if not db_member:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thành viên phù hợp.")
    db.delete(db_member)
    db.commit()
    return {"detail": "Đã xóa thành viên."}