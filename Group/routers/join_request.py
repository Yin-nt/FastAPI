from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, schemas
from Group.crud import crud_join, crud_user, crud_member
from Group.core import oauth2
router = APIRouter(
    tags=["Join request"]
)
get_db = database.get_db


@router.post("/join_request", response_model=schemas.ShowJoinRequest)
def create_join_request(join_request: schemas.CreatJoinRequest,
                        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    if join_request.inviter_id is None:
        if crud_member.is_member(db, user.id, join_request.group_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bạn đã là thành viên của nhóm.")
        if crud_join.is_pending_request(db, invitee_id=user.id, group_id=join_request.group_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bạn đã có một lời mời đang chờ xử lý.")
        join_request.invitee_id = user.id
        return crud_join.create_request(db=db, join_request=join_request)
    # inviter không ở trong group
    if not crud_member.is_member(db, user.id, join_request.group_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bạn không có quyền tạo lời mời.")
    # invitee đã được mời chưa
    if crud_join.is_pending_request(db, invitee_id=join_request.invitee_id, group_id=join_request.group_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User đã được mời")
    # invitee đã ở trong group
    if crud_member.is_member(db, join_request.invitee_id, join_request.group_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người mời đã ở trong group.")
    return crud_join.create_request(db=db, join_request=join_request)


@router.put("/join_request/{request_id}", response_model=schemas.ShowJoinRequest)
def update_join_request(update_data: schemas.JoinRequestUpdate,
                        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    db_join_request = crud_join.update_request(db, update_data=update_data)
    if not db_join_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lời mời")
    return db_join_request


@router.put("/approve_join_request/{request_id}", response_model=schemas.ShowJoinRequest)
def approve_join_request(
        update_data: schemas.JoinRequestUpdate,
        current_user: schemas.TokenData = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    # kiểm tra request có tồn tại trong database không
    request = crud_join.get_request(db=db, invitee_id=update_data.invitee_id, group_id=update_data.group_id)
    if not request:
        raise HTTPException(status_code=404, detail="Không tìm thấy lời mời.")
    # tìm member theo group và user id
    member = crud_member.get_member_by_user_and_group_id(db=db, user_id=user.id, group_id=request.group_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không phải là thành viên của nhóm.")
    if not crud_member.is_admin(db=db, user_id=user.id, group_id=member.group_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ admin mới có quyền được duyệt.")
    invitee = crud_member.get_member_by_user_and_group_id(
        db=db, user_id=request.invitee_id, group_id=request.group_id)
    crud_member.update_member(db=db, user_id=invitee.user_id, group_id=invitee.group_id)
    return request


# người mời hoặc người nhận tự join vào group (chưa accepted) mới được xóa
@router.delete("/join_request/{join_request_id}")
def delete_request(join_request_id: int, db: Session = Depends(get_db),
                   current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy user")
    join_request = crud_join.get_request_by_id(db=db, request_id=join_request_id)
    if not join_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lời mời")
    if join_request.inviter_id != user.user_id and join_request.inviter_id is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không thể xóa lời mời.")
    if join_request.inviter_id is None and join_request.invitee_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không thể xóa lời mời.")
    db.delete(join_request)
    db.commit()
    return {"detail": "Bạn đã xóa lời mời thành công."}