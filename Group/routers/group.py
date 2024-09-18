from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.crud import crud_group, crud_member, crud_user
import Group.core.oauth2 as oauth2

router = APIRouter(
    tags=["Group"]
)
get_db = database.get_db
@router.post("/groups", response_model=schemas.ShowGroup)
def create_group(group: schemas.CreateGroup, db: Session = Depends(get_db),
                 current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng.")
    db_group = crud_group.get_group_by_name(db, group_name=group.group_name)
    if db_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Tên nhóm đã tồn tại")
    return crud_group.create_group(db=db, group=group, user_id=user.id)

@router.delete('/group/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(group_id: int, db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng.")
    if not crud_member.is_admin(db, user.id, group_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xóa group.")
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(detail='Không tìm thấy group.',status_code=status.HTTP_404_NOT_FOUND)
    db.delete(group)
    db.commit()
    return {'detail': 'Group đã được xóa.'}
@router.get("/{group_id}", response_model=schemas.ShowGroup)
def read_infor_group(group_id: int, db: Session = Depends(get_db),
                     current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    db_group = crud_group.get_group(db, id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy group.")
    return db_group


@router.put("/{group_id}", response_model=schemas.ShowGroup)
def fixed_group_name(group_name: str, new_group_name: str, db: Session = Depends(get_db),
                       current_user: schemas.TokenData =Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db, email=current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    group = crud_group.get_group_by_name(db=db, group_name=group_name)
    if not group:
        raise HTTPException(status_code=404, detail="Không tìm thấy group.")
    member = crud_member.get_member_by_user_and_group_id(db=db, user_id=user.id, group_id=group.id)
    if not member:
        raise HTTPException(status_code=404, detail="Bạn chưa là thành viên của nhóm.")
    if not crud_member.is_admin(db=db, user_id=user.id, group_id=group.id):
        raise HTTPException(status_code=403, detail="Bạn không có quyền thay đổi tên group")
    return crud_group.fixed_group_name(db=db, group_name=group_name, new_group_name=new_group_name)