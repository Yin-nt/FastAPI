#Các hàm để tương tác với dữ liệu (Crud = Creat, read, update, delete)
from sqlalchemy.orm import Session #chấp nhận khai báo tham số db

from . import models, schemas

#đọc 1 user bằng id
#db: Session là một phiên làm việc SQLAlchemy được tiêm vào (injected) vào hàm get_user thông qua dependency injection
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

#đọc 1 user bằng email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#đọc nhiều user
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
#offset(): số bản ghi bỏ qua tính từ đầu
#limit(): số lượng bản ghi tối đa trả về
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user) # Thêm vào database
    db.commit() # Lưu thay đổi
    db.refresh(db_user) #Làm mới
    return db_user

#đọc nhiều item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''
- By creating functions that are only dedicated to interacting with the database (get a user or an item) independent of 
your path operation function, you can more easily reuse them in multiple parts and also add unit tests for them.
?Dependency Injection
- db.query(): là phương thức trong SQLAlchemy tạo 1 truy vấn
- models.User(): là class user đc định nghĩa trong models 
'''