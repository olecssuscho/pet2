from fastapi import APIRouter,Depends
from schemas.models import WebhookMODEL,UserMODEL
from sqlalchemy.orm import Session
from dependency import get_current_user,get_db
from services.Webhook import webhook_post_service

router = APIRouter()

@router.post("/webhook/register")
def webhook_post(url:str = None,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return webhook_post_service(url,user,db)
