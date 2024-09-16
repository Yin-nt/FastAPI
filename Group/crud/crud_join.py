from sqlalchemy.orm import Session
from Group import models, schemas
from datetime import date


def create_request(db: Session, join_request: schemas.CreatJoinRequest):
    db_request = models.Join_request(
        inviter_id=join_request.inviter_id if join_request.inviter_id else None,
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
    if db_request.status == "Accepted":
        existing_member = db.query(models.Group_member).filter(
            models.Group_member.user_id == db_request.invitee_id,
            models.Group_member.group_id == db_request.group_id).first()
        if not existing_member:
            new_member = models.Group_member(
                user_id=db_request.invitee_id,
                group_id=db_request.group_id,
                role_id=2,
                is_approve=False,
                join_date=date.today()
            )
            db.add(new_member)
            db.commit()
            db.refresh(new_member)
    return db_request


def get_request(db: Session, request_id: int):
    return db.query(models.Join_request).filter(models.Join_request.id == request_id).first()
