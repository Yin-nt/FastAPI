from sqlalchemy.orm import Session
from Group import models, schemas
from sqlalchemy import and_


def create_member(db: Session, member: schemas.CreateMember):
    user_exists = db.query(models.User).filter(models.User.id == member.user_id).first()
    group_exists = db.query(models.Group).filter(models.Group.id == member.group_id).first()
    role_exists = db.query(models.Role).filter(models.Role.id == member.role_id).first()
    if not user_exists:
        raise ValueError("User không tồn tại.")
    if not group_exists:
        raise ValueError("Group không tồn tại.")
    if not role_exists:
        raise ValueError("Role không tồn tại.")
    db_member = models.Group_member(
        user_id=member.user_id,
        group_id=member.group_id,
        role_id=member.role_id,
        is_approve=False,
        join_date=member.join_date
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member_by_id(db: Session, member_id: int):
    return db.query(models.Group_member).filter(models.Group_member.id == member_id).first()


def get_all_members(db: Session, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Group_member).filter(
        models.Group_member.group_id == group_id).offset(skip).limit(limit).all()


def get_member_by_user_and_group_id(db: Session, user_id: int, group_id: int):
    return db.query(models.Group_member).filter(and_(
            models.Group_member.user_id == user_id,
            models.Group_member.group_id == group_id
        )
    ).first()


def get_member_by_user_id(db: Session, user_id: int):
    return db.query(models.Group_member).filter(models.Group_member.user_id == user_id).first()


def is_admin(db: Session, user_id: int, group_id: int):
    member = db.query(models.Group_member).filter(
        models.Group_member.user_id == user_id,
        models.Group_member.group_id == group_id
    ).first()
    if not member:
        return False
    role = db.query(models.Role).filter(models.Role.id == member.role_id).first()
    return role.role_name == "admin"


def is_member(db: Session, inviter_id: int, group_id: int, is_approved: bool = True):
    member = db.query(models.Group_member).filter(
        models.Group_member.group_id == group_id,
        models.Group_member.user_id == inviter_id)
    if is_approved:
        member = member.filter(models.Group_member.is_approve == True)
    result = member.first()
    if result is None:
        return False
    return True


def update_member(db: Session, user_id: int, group_id: int):
    member = db.query(models.Group_member).filter(models.Group_member.user_id == user_id,
                                                  models.Group_member.group_id == group_id).first()
    member.is_approve = True
    db.commit()
    db.refresh(member)
    return member
