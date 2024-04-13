from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update #, delete
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
import logging

from db import models

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_knowledge_request(db: Session, user_id: int, content: str, file_url=None, file_type='text'):
    db_request = models.KnowledgeRequest(user_id=user_id, content=content, file_url=file_url, file_type=file_type, timestamp=datetime.utcnow())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def edit_knowledge_request(db: Session, request_id: int, content: str):
    db_request = db.execute(select(models.KnowledgeRequest).where(models.KnowledgeRequest.id == request_id)).scalars().first()
    db_request.content = content
    db.commit()
    db.refresh(db_request)
    return db_request


def get_knowledge_request(db: Session, request_id: int):
    return db.execute(select(models.KnowledgeRequest).where(models.KnowledgeRequest.id == request_id)).scalars().first()

def get_knowledge_requests(db: Session):
    return db.execute(select(models.KnowledgeRequest).order_by(models.KnowledgeRequest.timestamp.desc())).scalars().all()

def add_response_to_request(db: Session, request_id: int, user_id: int, content: str, file_url=None, file_type='text'):
    db_response = models.Response(request_id=request_id, user_id=user_id, content=content, file_url=file_url, file_type=file_type, timestamp=datetime.utcnow())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def edit_response(db: Session, response_id: int, content: str):
    db_response = db.execute(select(models.Response).where(models.Response.id == response_id)).scalars().first()
    db_response.content = content
    db.commit()
    db.refresh(db_response)
    return db_response


def get_response(db: Session, response_id: int):
    return db.execute(select(models.Response).where(models.Response.id == response_id)).scalars().first()

def get_responses_for_request(db: Session, request_id: int):
    return db.execute(select(models.Response).where(models.Response.request_id == request_id).order_by(models.Response.timestamp.asc())).scalars().all()

def create_user(db: Session, tg_id: int, tg_name: str, name: str = None):
    db_user = models.User(tg_id=tg_id, tg_name=tg_name, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int = None, tg_id: int = None):
    query = select(models.User)
    if user_id:
        return db.execute(query.where(models.User.id == user_id)).scalars().first()
    elif tg_id:
        return db.execute(query.where(models.User.tg_id == tg_id)).scalars().first()
        return None

def add_or_update_vote(session: Session, model, object_id, user_id, vote_value):
    vote = session.query(model).filter_by(object_id=object_id, user_id=user_id).first()
    if vote:
        vote.vote = vote_value
    else:
        vote = model(object_id=object_id, user_id=user_id, vote=vote_value)
        session.add(vote)
        session.commit()

def get_sorted_knowledge_requests(session: Session):
    return db.execute(select(KnowledgeRequest, func.sum(RequestVote.vote).label("votes")).join(RequestVote)..order_by(KnowledgeRequest.id).order_by("votes").all()

def get_sorted_responses(session: Session, request_id):
    return session.query(Response, func.sum(ResponseVote.vote).label("votes")).join(ResponseVote).filter(Response.request_id == request_id).group_by(Response.id).order_by("votes").all()

def add_tags_to_request(session: Session, request_id: int, tag_names: list):
    request = session.query(KnowledgeRequest).get(request_id)
    for tag_name in tag_names:
        tag = session.query(Tag).filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
    session.add(tag)
        if tag not in request.tags:
            request.tags.append(tag)
    session.commit()

def get_requests_by_tag(session: Session, tag_name: str):
        return session.query(KnowledgeRequest).join(KnowledgeRequest.tags).filter(Tag.name == tag_name).all()


def subscribe_to_tag(session: Session, user_id: int, tag_id: int):
    try:
        subscription = Subscription(user_id=user_id, tag_id=tag_id, subscription_type="tag", active=True)
        session.add(subscription)
        session.commit()

def subscribe_to_responses(session: Session, user_id: int):
        subscription = Subscription(user_id=user_id, subscription_type="response", active=True)
        session.add(subscription)
        session.commit()

def unsubscribe(session: Session, user_id: int, subscription_id: int):
        subscription = session.query(Subscription).filter_by(id=subscription_id, user_id=user_id).first()
        if subscription:
            session.delete(subscription)
        session.commit()


def authenticate_admin(session: Session, login: str, password_hash: str):
    try:
        admin = session.query(models.Admin).filter_by(login=login, password_hash=password_hash).first()
        return admin is not None

def get_pending_requests(session: Session):
        return session.query(models.KnowledgeRequest).filter_by(approved=False).all()

def approve_request(session: Session, request_id: int):
    request = session.query(models.KnowledgeRequest).get(request_id)
    request.approved = True
    session.commit()

def reject_request(session: Session, request_id: int):
    session.delete(session.query(models.KnowledgeRequest).get(request_id))
    session.commit()
