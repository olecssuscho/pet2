from schemas.dbmodels import WebhookDB,UserDB,WebhookLogDB
from sqlalchemy.orm import Session
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

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
    db.delete(db.query(WebhookDB).filter(WebhookDB.id == id).first())
    db.commit()
    return "Success"

@retry(stop = stop_after_attempt(3),wait=wait_exponential(multiplier=1,min=1,max=30),retry=retry_if_exception_type(httpx.RequestError),reraise=True)
def post_webhook_on_url(URL:str,result:str,user_id:int,db:Session):
    r = httpx.post(url=URL,content=result)
    webhook = db.query(WebhookDB).filter(WebhookDB.user_id == user_id).first()
    db.flush()
    db.add(WebhookLogDB(
        webhook_id = webhook.id,
        responce_status = r.status_code
    ))
    db.commit()