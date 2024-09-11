from pydantic import BaseModel, Field
from typing import List, Union
from enum import Enum
from datetime import date

class UserBase(BaseModel):
    email: str
class CreateUser(UserBase):
    password: str
    fullname: str
    DOB: date
    address: str

class ShowUser(UserBase):
    fullname: str
    DOB: date
    address: str
    class Config:
        from_attributes = True
class User(BaseModel):
    id: int
    email: str
    fullname: str
    DOB: date
    address: str
    class Config:
        from_attributes = True
class GroupBase(BaseModel):
    group_name: str

class CreateGroup(GroupBase):
    pass

class ShowGroup(GroupBase):
    pass
class GroupMemberBase(BaseModel):
    user_id: int
    group_id: int
    role_id: int
    join_date: date

class CreateMember(BaseModel):
    is_approve: bool
    group_id: int
    user_id: int
    role_id: int
    join_date: date

class ShowMember(GroupMemberBase):
    pass

class ShowMembers(BaseModel):
    members: List[ShowMember]


class JoinRequestStatus(str, Enum):
    accepted = 'accepted'
    rejected = 'rejected'
    pending = 'pending'
    self_joined = 'self joined'

class JoinRequestBase(BaseModel):
    inviter_id: Union[int, None] = None
    invitee_id: int
    group_id: int
    creat_at: date
    status: JoinRequestStatus

class CreatJoinRequest(JoinRequestBase):
    pass
class JoinRequestUpdate(BaseModel):
    status: JoinRequestStatus # Cap nhat trang thai tham gia nhom

class ShowJoinRequest(JoinRequestBase):
    inviter: Union['ShowUser', None] = None
    invitee: 'ShowUser'
    Group: 'ShowGroup'
    class Config:
        from_attributes = True
class RoleBase(BaseModel):
    role_name: str

class ShowRole(RoleBase):
    id: int
    class Config:
        from_attributes = True
class CreateRole(RoleBase):
    pass

class TypeReaction(str, Enum):
    like = 'Like'
    dislike = 'Dislike'
    sad = 'Sad'
    haha = 'Haha'
class ReactionBase(BaseModel):
    user_id: int
    group_id: int
    blog_id: int
    type_reaction: TypeReaction

class ReactionCreate(ReactionBase):
    pass
class ReactionUpdate(ReactionBase):
    type_reaction: TypeReaction
class ReactionShow(ReactionBase):
    reaction_id: int

class BlogBase(BaseModel):
    title: str
    content: str
    group_id: int
    author_id: int

class CreatBlog(BlogBase):
    permission: bool = False
    creat_at: date = Field(default=date.today())
    update_at: date = Field(default=date.today())
class ShowBlog(BlogBase):
    creat_at: date = Field(default=date.today())
    update_at: date = Field(default=date.today())

class Login(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
