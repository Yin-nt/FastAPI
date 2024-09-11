from sqlalchemy.orm import Session
from Group import models, schemas

def create_group(db: Session, group: schemas.CreateGroup):
    db_group = models.Group(group_name=group.group_name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
def get_group(db: Session, id: int):
    return db.query(models.Group).filter(models.Group.id == id).first()
def get_group_by_name(db: Session, group_name: str):
    return db.query(models.Group).filter(models.Group.group_name == group_name).first()
