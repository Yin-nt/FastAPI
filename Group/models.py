from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from Group.database import Base

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255))
    fullname = Column(String(255))
    DOB = Column(Date)
    address = Column(String(255))

    # Relationships
    groups = relationship("Group", secondary="Group_member", back_populates="members")
    blogs = relationship("Blog", back_populates="author")
    sent_requests = relationship("Join_request", foreign_keys="[Join_request.inviter_id]", back_populates="inviter")
    received_requests = relationship("Join_request", foreign_keys="[Join_request.invitee_id]", back_populates="invitee")
    reactions = relationship("Reaction", back_populates="user")


class Group(Base):
    __tablename__ = "Group"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(255), unique=True, nullable=False)

    # Relationships
    members = relationship("User", secondary="Group_member", back_populates="groups")
    blogs = relationship("Blog", back_populates="group")
    join_requests = relationship("Join_request", back_populates="group")


class Group_member(Base):
    __tablename__ = 'Group_member'
    id = Column(Integer, primary_key=True)
    is_approve = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('Role.id'))
    group_id = Column(Integer, ForeignKey('Group.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    join_date = Column(Date)

    # Relationships
    user = relationship("User")
    group = relationship("Group")
    role = relationship("Role")


class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(255), nullable=False)

    # Relationships
    group_members = relationship("Group_member", back_populates="role")


class Blog(Base):
    __tablename__ = 'Blog'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'))
    group_id = Column(Integer, ForeignKey('Group.id'))
    permission = Column(Boolean, default=False)  # private
    creat_at = Column(DateTime, default=datetime)
    update_at = Column(DateTime, default=datetime)

    # Relationships
    author = relationship("User", back_populates="blogs")
    group = relationship("Group", back_populates="blogs")
    reactions = relationship("Reaction", back_populates="blog")


class Join_request(Base):
    __tablename__ = "Join_request"
    id = Column(Integer, primary_key=True)
    inviter_id = Column(Integer, ForeignKey('User.id'), nullable=True)
    invitee_id = Column(Integer, ForeignKey('User.id'))
    group_id = Column(Integer, ForeignKey('Group.id'))
    status = Column(Enum('Accepted', 'Rejected', 'Pending', 'Self join'), default='Pending')
    creat_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inviter = relationship("User", foreign_keys=[inviter_id], back_populates="sent_requests")
    invitee = relationship("User", foreign_keys=[invitee_id], back_populates="received_requests")
    group = relationship("Group", back_populates="join_requests")


class Reaction(Base):
    __tablename__ = 'Reaction'
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey('Blog.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    creat_at = Column(DateTime, default=datetime.utcnow)
    type = Column(Enum('Like', 'dislike', 'sad', 'haha'))

    # Relationships
    blog = relationship("Blog", back_populates="reactions")
    user = relationship("User", back_populates="reactions")
