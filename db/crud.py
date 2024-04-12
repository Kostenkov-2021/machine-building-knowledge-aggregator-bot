from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
import logging
from db import models
from models import KnowledgeRequest, Tag

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_knowledge_request(db: Session, user_id: int, content: str):
    try:
        db_request = models.KnowledgeRequest(user_id=user_id, content=content, timestamp=datetime.utcnow())
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating knowledge request: {e}")
        raise

def edit_knowledge_request(db: Session, request_id: int, content: str):
    try:
        db_request = db.get(models.KnowledgeRequest, request_id)
        if db_request:
            db_request.content = content
            db.commit()
            db.refresh(db_request)
            return db_request
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error editing knowledge request: {e}")
        raise


def get_knowledge_request(db: Session, request_id: int):
    try:
        return db.get(models.KnowledgeRequest, request_id)
    except SQLAlchemyError as e:
        logger.error(f"Error getting knowledge request: {e}")
        raise

def get_knowledge_requests(db: Session):
    try:
        return db.execute(select(models.KnowledgeRequest).order_by(models.KnowledgeRequest.timestamp.desc())).scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting knowledge requests: {e}")
        raise

def add_response_to_request(db: Session, request_id: int, user_id: int, content: str):
    try:
        db_response = models.Response(request_id=request_id, user_id=user_id, content=content, timestamp=datetime.utcnow())
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        return db_response
    except SQLAlchemyError as e:
        logger.error(f"Error adding response to request: {e}")
        raise

def edit_response(db: Session, response_id: int, content: str):
    try:
        db_response = db.execute(select(models.Response).where(models.Response.id == response_id)).scalars().first()
        db_response.content = content
        db.commit()
        db.refresh(db_response)
        return db_response
    except SQLAlchemyError as e:
        logger.error(f"Error editing response: {e}")
        raise

def get_response(db: Session, response_id: int):
    try:
        return db.execute(select(models.Response).where(models.Response.id == response_id)).scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting response: {e}")
        raise

def get_responses_for_request(db: Session, request_id: int):
    try:
        return db.execute(select(models.Response).where(models.Response.request_id == request_id).order_by(models.Response.timestamp.asc())).scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting responses for request: {e}")
        raise

def create_user(db: Session, tg_id: int, tg_name: str, name: str = None):
    try:
        db_user = models.User(tg_id=tg_id, tg_name=tg_name, name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error creating user: {e}")
        raise

def get_user(db: Session, user_id: int = None, tg_id: int = None):
    try:
        query = select(models.User)
        if user_id:
            return db.execute(query.where(models.User.id == user_id)).scalars().first()
        elif tg_id:
            return db.execute(query.where(models.User.tg_id == tg_id)).scalars().first()
        return None
    except SQLAlchemyError as e:
        logger.error(f"Error getting user: {e}")
        raise

def add_or_update_vote(session: Session, model, object_id, user_id, vote_value):
    try:
        vote = session.query(model).filter_by(object_id=object_id, user_id=user_id).first()
        if vote:
            vote.vote = vote_value
        else:
            vote = model(object_id=object_id, user_id=user_id, vote=vote_value)
            session.add(vote)
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error adding or updating vote: {e}")
        raise

def get_sorted_knowledge_requests(session: Session):
    try:
        return session.query(KnowledgeRequest, func.sum(RequestVote.vote).label("votes")).join(RequestVote).group_by(KnowledgeRequest.id).order_by("votes").all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting sorted knowledge requests: {e}")
        raise

def get_sorted_responses(session: Session, request_id):
    try:
        return session.query(Response, func.sum(ResponseVote.vote).label("votes")).join(ResponseVote).filter(Response.request_id == request_id).group_by(Response.id).order_by("votes").all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting sorted responses: {e}")
        raise

def add_tags_to_request(session: Session, request_id: int, tag_names: list):
    try:
        request = session.query(KnowledgeRequest).get(request_id)
        for tag_name in tag_names:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            if tag not in request.tags:
                request.tags.append(tag)
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error adding tags to request: {e}")
        raise

def get_requests_by_tag(session: Session, tag_name: str):
    try:
        return session.query(KnowledgeRequest).join(KnowledgeRequest.tags).filter(Tag.name == tag_name).all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting requests by tag: {e}")
        raise
