from schemas.dbmodels import WebhookDB,UserDB
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status,HTTPException

def webhook_post_service(url:str,user:UserDB,db:Session):
    Webhook = WebhookDB(
        url = url,
        user_id = user.id
    )
    db.add(Webhook)
    db.commit()
    return "Success"

def webhook_get_service(user:UserDB,db:Session):
    return db.query(WebhookDB).filter(WebhookDB.user_id == user.id).all()

def webhook_delete_service(id:int,user:UserDB,db:Session):
    db.delete(db.query(WebhookDB).filter(WebhookDB.id == id).first())
    db.commit()
    return "Success"