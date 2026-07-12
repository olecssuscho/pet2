from typing import List

from database import SessionLocal
from schemas.dbmodels import WebhookDB,UserDB,WebhookLogDB,EmailLogDB
from sqlalchemy.orm import Session
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from fastapi import HTTPException,status
from fastapi_mail import MessageSchema,ConnectionConfig,FastMail,MessageType
from config import settings

def webhook_post_service(url:str,email:str,user:UserDB,db:Session):
    Webhook = WebhookDB(
        url = url,
        user_id = user.id,
        email = email
    )
    db.add(Webhook)
    db.commit()
    return "Success"

def webhook_get_service(user:UserDB,db:Session):
    return db.query(WebhookDB).filter(WebhookDB.user_id == user.id).all()

def webhook_delete_service(user:UserDB,id:int,db:Session):
    if db.query(WebhookDB).filter((WebhookDB.id == id),(WebhookDB.user_id == user.id)).first():
        db.delete(db.query(WebhookDB).filter(WebhookDB.id == id).first())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Your webhook not found")
    db.commit()
    return "Success"

def post_webhook_on_url_services(URL: str, result: str, user_id: int):
    db = SessionLocal()
    try:
        attempt = 0
        target = db.query(WebhookDB).filter(WebhookDB.user_id == user_id).first()
        target.failure_count = 0
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=1, max=30),
            retry=retry_if_exception_type(httpx.RequestError),
            reraise=True
        )
        def _send():
            nonlocal attempt
            attempt += 1
            target.failure_count += 1
            if target.failure_count >= 3:
                target.is_active = False
                target.deactivated_at 
            r = httpx.post(url=URL, content=result)
            webhook = db.query(WebhookDB).filter(WebhookDB.user_id == user_id).first()
            db.add(WebhookLogDB(
                webhook_id=webhook.id,
                responce_status=r.status_code,
                attempt_number=attempt
            ))
            db.commit()

        _send()
    finally:
        db.close()

async def webhook_post_email_services(email:str,result:str,user_id:int,db:Session):
    attempt = 0
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True
    )
    async def _send():
        nonlocal attempt
        attempt += 1
        conf = ConnectionConfig(
        MAIL_FROM= settings.MAIL_FROM,
        MAIL_PORT= settings.MAIL_PORT,
        MAIL_PASSWORD= settings.MAIL_PASSWORD,
        MAIL_SERVER= settings.MAIL_SERVER,
        MAIL_USERNAME= settings.MAIL_USERNAME,
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
        )

        recipients = email if isinstance(email, list) else [email]

        message = MessageSchema(
            subject="FastApi-Mail Module",
            recipients=recipients,
            body=result,
            subtype=MessageType.html
        )
    
        fm = FastMail(conf)

        try:
            await fm.send_message(message)
            response_status = "success"
        except Exception as e:
            response_status = f"failed: {str(e)}"
        webhook = db.query(WebhookDB).filter(WebhookDB.user_id == user_id).first()
        db.add(EmailLogDB(
            webhook_id=webhook.id,
            responce_status=response_status,
            attempt_number=attempt
        ))
        db.commit()

    await _send()
    return "Message was sent"
















