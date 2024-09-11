from sqlalchemy.orm import Session
from Group import database, models, schemas

def create_role(db: Session, role: schemas.CreateRole):
    db_role = models.Role(
        role_name=role.role_name,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role(db: Session, id: int):
    return db.query(models.Role).filter(models.Role.id == id).first()
# def get_role_by_user_and_group_id( db: Session, user_id: int, group_id: int):
#     db.query(models.Role).filter(models.Role.user_id == user_id and models.Role.group_id == group_id).first()
# def get_role_by_user_id(db: Session, user_id: int, skip:int, limit: int):
#     return db.query(models.Role).filter(models.Role.user_id == user_id).offset(skip).limit(limit).all()