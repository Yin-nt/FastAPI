#Tệp chứa các mô hình Pydantic (định nghĩa một schema)
from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True

'''
- Phân biệt SQLAlchemy và Pydantic:
    SQLAlchemy: name = Column(String)
    Pydantic: name: str 
- orm_mode = True: đọc dữ liệu mặc dù không phải là dict ( id = data['id'] tương tự id = data.id)
- SQLAlchemy là 'lazy loading': không lấy dữ liệu trừ khi truy cập vào thuộc tính
- Nếu không có orm_mode, khi trả về 1 SQLAlchemy model từ path operation sẽ không gồm relationship data


'''