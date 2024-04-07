from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


# Таблица для связи многие-ко-многим между запросами и тегами
request_tags_table = Table('request_tags', Base.metadata,
    Column('request_id', ForeignKey('knowledge_requests.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    contact_info = Column(String)

    requests = relationship("KnowledgeRequest", back_populates="user", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", order_by=Subscription.id)
    notification_history = relationship("NotificationHistory", back_populates="user", order_by="desc(NotificationHistory.timestamp)")
    admin = relationship("Admin", back_populates="user")


class KnowledgeRequest(Base):
    __tablename__ = "knowledge_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    user = relationship("User", back_populates="requests")
    tags = relationship("Tag", secondary=request_tags_table, back_populates="requests")
    responses = relationship("Response", back_populates="request", cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("knowledge_requests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    request = relationship("KnowledgeRequest", back_populates="responses")
    user = relationship("User", back_populates="responses")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    requests = relationship("KnowledgeRequest", secondary=request_tags_table, back_populates="tags")
    subscriptions = relationship("Subscription", back_populates="tag", order_by=Subscription.id)


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    active = Column(Integer, default=1)  # 0 for inactive, 1 for active

    user = relationship("User", back_populates="subscriptions")
    tag = relationship("Tag", back_populates="subscriptions")


class NotificationHistory(Base):
    __tablename__ = "notification_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    user = relationship("User", back_populates="notification_history")


class RequestVote(Base):
    __tablename__ = "request_votes"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("knowledge_requests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    request = relationship("KnowledgeRequest")
    user = relationship("User")


class ResponseVote(Base):
    __tablename__ = "response_votes"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    response = relationship("Response")
    user = relationship("User")


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    user = relationship("User", back_populates="admin")
