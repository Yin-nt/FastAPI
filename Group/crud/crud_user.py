from sqlalchemy.orm import Session
from Group import database, models, schemas
from Group.core import hashing, oauth2

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
def create_user(db: Session, user: schemas.CreateUser):
    fake_hashed_password = hashing.Hash.bcrypt(user.password)
    db_user = models.User(
        email=user.email,
        password=fake_hashed_password,
        fullname = user.fullname,
        DOB = user.DOB,
        address = user.address)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def Update_info_user(db: Session, user_id: int, updated_data: schemas.UpdateInfoUser):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.fullname = updated_data.fullname
    user.DOB = updated_data.DOB
    user.address = updated_data.address
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user_id: int, new_password: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    fake_hashed_password = hashing.Hash.bcrypt(new_password)
    user.password = fake_hashed_password
    db.commit()
    db.refresh(user)
    return user

