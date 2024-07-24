#tệp chứa các models SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sql_app.database import Base
class User(Base):
    __tablename__ = "users"
    # __tablename__ : khai bao ten bang
    id = Column(Integer, primary_key=True)
    email = Column(String(255)  , unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

'''
Ý nghĩa các tham số:
    - unique: không có 2 hàng nào có dữ liệu giống nhau
    - index: thêm vào giúp truy vấn nhanh hơn (?) 
    - default: giá trị mặc định trong cột 
    - primary_key: khóa chính 
relationship: chứa các giá trị từ các bảng khác liên quan 
Đối với MySQl cần giới hạn độ dài string
'''