import enum
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, Enum, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base  # Импорт из orm
from sqlalchemy.dialects.sqlite import BLOB


SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

# создание движка
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

# Таблица для связи многие-ко-многим между запросами и тегами
request_tags_table = Table('request_tags', Base.metadata,
    Column('request_id', ForeignKey('knowledge_requests.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    contact_info = Column(String)
    is_admin = Column(Integer, default=0)  # 0 for false, 1 for true

class KnowledgeRequest(Base):
    __tablename__ = "knowledge_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vote_count = Column(Integer, default=0)

    user = relationship("User", back_populates="requests")
    tags = relationship("Tag", secondary=request_tags_table, back_populates="requests")
    responses = relationship("Response", back_populates="request")

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("knowledge_requests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vote_count = Column(Integer, default=0)

    request = relationship("KnowledgeRequest", back_populates="responses")
    user = relationship("User", back_populates="responses")

    class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

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
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notification_history")

# Расширение модели User для поддержки связей
User.subscriptions = relationship("Subscription", back_populates="user", order_by=Subscription.id)
User.notification_history = relationship("NotificationHistory", back_populates="user", order_by=NotificationHistory.timestamp)

Tag.subscriptions = relationship("Subscription", back_populates="tag", order_by=Subscription.id)




    requests = relationship("KnowledgeRequest", secondary=request_tags_table, back_populates="tags")

class ResponseVote(Base):
    __tablename__ = "response_votes"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    response = relationship("Response")
    user = relationship("User")

class AdminSection(Base):
    __tablename__ = "admin_section"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password_hash = Column(String)  # Хранение хэшированных паролей

# Расширение моделей User, KnowledgeRequest и Response для поддержки связей
User.requests = relationship("KnowledgeRequest", order_by=KnowledgeRequest.id, back_populates="user")
User.responses = relationship("Response", order_by=Response.id, back_populates="user")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
