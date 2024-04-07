from datetime import datetime

from sqlalchemy.orm import Session

from . import models


def create_knowledge_request(db: Session, user_id: int, content: str):
    db_request = models.KnowledgeRequest(
        user_id=user_id, content=content, timestamp=datetime.utcnow())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_knowledge_requests(db: Session):
    return db.query(models.KnowledgeRequest).order_by(models.KnowledgeRequest.timestamp.asc()).all()


def add_response_to_request(db: Session, request_id: int, user_id: int, content: str):
    db_response = models.Response(
        request_id=request_id, user_id=user_id, content=content, timestamp=datetime.utcnow())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_responses_for_request(db: Session, request_id: int):
    return db.query(models.Response).filter(models.Response.request_id == request_id).order_by(models.Response.timestamp.asc()).all()
