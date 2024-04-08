from datetime import datetime

from sqlalchemy.orm import Session

from db import models


def create_knowledge_request(db: Session, user_id: int, content: str):
    db_request = models.KnowledgeRequest(
        user_id=user_id, content=content, timestamp=datetime.utcnow())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def edit_knowledge_request(db: Session, request_id: int, content: str):
    db_request = db.query(models.KnowledgeRequest).filter(
        models.KnowledgeRequest.id == request_id).first()
    db_request.content = content
    db.commit()
    db.refresh(db_request)
    return db_request


def get_knowledge_request(db: Session, request_id: int):
    return db.query(models.KnowledgeRequest).filter(models.KnowledgeRequest.id == request_id).first()


def get_knowledge_requests(db: Session):
    return db.query(models.KnowledgeRequest).order_by(models.KnowledgeRequest.timestamp.asc()).all()


def add_response_to_request(db: Session, request_id: int, user_id: int, content: str):
    db_response = models.Response(
        request_id=request_id, user_id=user_id, content=content, timestamp=datetime.utcnow())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def edit_response(db: Session, response_id: int, content: str):
    db_response=db.query(models.Response).filter(models.Response.id == response_id).first()
    db_response.content = content
    db.commit()
    db.refresh(db_response)
    return db_response


def get_responses_for_request(db: Session, request_id: int):
    return db.query(models.Response).filter(models.Response.request_id == request_id).order_by(models.Response.timestamp.asc()).all()


def create_user(db: Session, tg_id: int, tg_name: str, name: str = None):
    db_user = models.User(tg_id=tg_id, tg_name=tg_name, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int = None, tg_id: int = None):
    query = db.query(models.User)
    if user_id:
        return query.filter(models.User.id == user_id).first()
    elif tg_id:
        return query.filter(models.User.tg_id == tg_id).first()
    return None
