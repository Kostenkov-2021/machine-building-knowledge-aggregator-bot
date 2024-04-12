from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from db.database import Base


# Таблица для связи многие-ко-многим между запросами и тегами
request_tags_table = Table("request_tags", Base.metadata,
    Column("request_id", ForeignKey("knowledge_requests.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    tg_name = Column(String, unique=True, nullable=False)
    tg_id = Column(Integer, unique=True, nullable=False)

    requests = relationship("KnowledgeRequest", back_populates="user", cascade="all, delete-orphan")
    responses = relationship(
        "Response", back_populates="user", cascade="all, delete-orphan")
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

    requests = relationship(
        "KnowledgeRequest", secondary=request_tags_table, back_populates="tags")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    active = Column(Boolean, default=True)


    user = relationship("User", back_populates="subscriptions")
    tag = relationship("Tag", back_populates="subscriptions")


User.subscriptions = relationship(
    "Subscription", back_populates="user", order_by=Subscription.id)
Tag.subscriptions = relationship(
    "Subscription", back_populates="tag", order_by=Subscription.id)


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
    vote = Column(Integer)  # +1 for upvote, -1 for downvote

    request = relationship("KnowledgeRequest", backref=backref("votes", cascade="all, delete-orphan"))
    user = relationship("User")

    __table_args__ = (UniqueConstraint('request_id', 'user_id', name='_request_user_uc'),)

class ResponseVote(Base):
    __tablename__ = "response_votes"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    vote = Column(Integer)  # +1 for upvote, -1 for downvote

    response = relationship("Response", backref=backref("votes", cascade="all, delete-orphan"))
    user = relationship("User")

    __table_args__ = (UniqueConstraint('response_id', 'user_id', name='_response_user_uc'),)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    user = relationship("User", back_populates="admin")
