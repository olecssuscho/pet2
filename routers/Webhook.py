from fastapi import APIRouter,Depends
from schemas.models import WebhookMODEL,UserMODEL
from sqlalchemy.orm import Session
from dependency import get_current_user,get_db
from services.Webhook import webhook_post_service,webhook_get_service,webhook_delete_service

router = APIRouter()

@router.post("/webhook/register")
def webhook_post(url:str = None,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_post_service(url,user,db)

@router.get("/webhook")
def webhook_get(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_get_service(user,db)

@router.delete("/webhook/{id}")
def webhook_delete(id:int,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_delete_service(id,user,db)