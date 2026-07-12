from fastapi import APIRouter,Depends
from schemas.models import UserMODEL
from sqlalchemy.orm import Session
from dependency import get_current_user,get_db
from services.Webhook import (
    webhook_post_service,
    webhook_get_service,
    webhook_delete_service,
    post_webhook_on_url_services,
    webhook_post_email_services)

router = APIRouter(prefix="/webhook", tags=["Webhooks"])

@router.post("/webhook/register")
def webhook_post(url:str = None,email:str = None,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_post_service(url,email,user,db)

@router.get("/webhook")
def webhook_get(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_get_service(user,db)

@router.delete("/webhook/{id}")
def webhook_delete(id:int,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_delete_service(user,id,db)

@router.post("/webhook/url/post")
def webhook_post_url(url:str = None,result:str = None,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return post_webhook_on_url_services(url,result,user.id)

@router.post("/webhook/email/post")
async def webhook_post_email(result:str,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    await webhook_post_email_services(user.email,result,user.id,db)