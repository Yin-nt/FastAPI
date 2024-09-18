from sqlalchemy.orm import Session
from Group import models, schemas
from datetime import date


def create_group(db: Session, group: schemas.CreateGroup, user_id: int):
    db_group = models.Group(group_name=group.group_name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    new_member = models.Group_member(
        user_id=user_id,
        group_id=db_group.id,
        role_id=1,
        is_approve=True,
        join_date=date.today()
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return db_group


def get_group(db: Session, id: int):
    return db.query(models.Group).filter(models.Group.id == id).first()


def get_group_by_name(db: Session, group_name: str):
    return db.query(models.Group).filter(models.Group.group_name == group_name).first()


def fixed_group_name(db: Session, group_name: str, new_group_name: str):
    group = db.query(models.Group).filter(models.Group.group_name == group_name).first()
    group.group_name = new_group_name
    db.commit()
    db.refresh(group)
    return group
