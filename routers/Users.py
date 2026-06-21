from schemas.models import UserMODEL
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends,APIRouter,Header
from fastapi.security import OAuth2PasswordRequestForm
from dependency import get_db,get_current_user
from services.Users import register_service,login_services,get_user_services,refresh_services,get_stats_services,get_transactions_services

router = APIRouter()

@router.post("/register")
def register(user:UserMODEL,db:Session = Depends(get_db)) -> str:
    return register_service(user,db)

@router.post("/user/login")
def login(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    return login_services(form_data,db)

@router.get("/user/get/me")
def get_user(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_user_services(user,db)

@router.get("/user/refresh")
def refresh(token: str | None = Header(None),db:Session = Depends(get_db)):
    return refresh_services(token,db)

@router.get("/users/stats")
def get_stats(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_stats_services(user,db)

@router.get("/user/get")
def get_transactions(from_date:datetime = None,to_date:datetime = None,status:str = None,type:str = None, user: UserMODEL = Depends(get_current_user), db:Session = Depends(get_db)):
    return get_transactions_services(from_date,to_date,status,type,user,db)