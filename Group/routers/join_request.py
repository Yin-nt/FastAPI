from urllib import request

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.crud import crud_join, crud_member, crud_user, crud_member
from Group.core import oauth2
router = APIRouter(
    tags=["Join request"]
)
get_db = database.get_db
@router.post("/join_request", response_model=schemas.ShowJoinRequest)
def create_join_request(join_request: schemas.CreatJoinRequest,
                        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    inviter = crud_user.get_user_by_email(db, email=current_user.username)
    if not crud_member.is_member(db, inviter.id, join_request.group_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bạn không có quyền tạo lời mời.")
    if crud_member.is_member(db, join_request.invitee_id, join_request.group_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người mời đã ở trong group.")
    return crud_join.create_request(db=db, join_request=join_request)
@router.put("/join_request/{request_id}", response_model=schemas.ShowJoinRequest)
def update_join_request(request_id: int, update_data: schemas.JoinRequestUpdate,
                        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    db_join_request = crud_join.update_request(db, request_id=request_id, update_data=update_data)
    if not db_join_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_join_request
@router.put("/approve_join_request/{request_id}", response_model=schemas.ShowJoinRequest)
def approve_join_request(
        request_id: int, update_data: schemas.JoinRequestUpdate,
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    #tìm member theo group và user id
    member = crud_member.get_member_by_user_id(db=db, user_id=user.id)
    if not crud_member.is_admin(db=db, user_id=user.id, group_id=member.group_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ admin mới có quyền được duyệt.")
    join_request = crud_join.update_request(db=db, request_id=request_id, update_data=update_data)
    if not join_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return join_request
