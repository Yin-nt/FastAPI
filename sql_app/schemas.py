#Tệp chứa các mô hình Pydantic (định nghĩa một schema), chưá dữ liệu trả về
from typing import Union, List

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

#response model => khi trả về dữ liệu trên doc không có password
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True
class ShowUsers(BaseModel):
    email: str
    items: list[Item] = []

class Login(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
'''
- Phân biệt SQLAlchemy và Pydantic:
    SQLAlchemy: name = Column(String)
    Pydantic: name: str 
- orm_mode = True: đọc dữ liệu mặc dù không phải là dict ( id = data['id'] tương tự id = data.id)
- SQLAlchemy là 'lazy loading': không lấy dữ liệu trừ khi truy cập vào thuộc tính
- Nếu không có orm_mode, khi trả về 1 SQLAlchemy model từ path operation sẽ không gồm relationship data


'''