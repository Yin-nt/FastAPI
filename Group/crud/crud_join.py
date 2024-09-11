from sqlalchemy.orm import Session
from Group import models, schemas
from typing import Union

def create_request(db: Session, join_request: schemas.CreatJoinRequest):
    db_request = models.Join_request(
        inviter_id=join_request.inviter_id,
        invitee_id=join_request.invitee_id,
        group_id=join_request.group_id,
        creat_at=join_request.creat_at,
        status=join_request.status
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def update_request(db: Session, request_id: int, update_data: schemas.JoinRequestUpdate):
    db_request = db.query(models.Join_request).filter(models.Join_request.id == request_id).first()
    if db_request:
        db_request.status = update_data.status
        db.commit()
        db.refresh(db_request)
    return db_request

