from schemas.dbmodels import WebhookDB,UserDB,WebhookLogDB
from sqlalchemy.orm import Session
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from fastapi import HTTPException,status

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

def webhook_delete_service(id:int,db:Session):
    if db.query(WebhookDB).filter(WebhookDB.id == id).first():
        db.delete(db.query(WebhookDB).filter(WebhookDB.id == id).first())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Your webhook not found")
    db.commit()
    return "Success"

def post_webhook_on_url(URL: str, result: str, user_id: int, db: Session):
    attempt = 0
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True
    )
    def _send():
        nonlocal attempt
        attempt += 1
        r = httpx.post(url=URL, content=result)
        webhook = db.query(WebhookDB).filter(WebhookDB.user_id == user_id).first()
        db.add(WebhookLogDB(
            webhook_id=webhook.id,
            responce_status=r.status_code,
            attempt_number=attempt
        ))
        db.commit()
    
    _send()