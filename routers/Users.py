from schemas.models import User
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from dependency import get_db
from services.Users import register_service
from schemas.responces import UserResponce

router = APIRouter()

@router.post("/register")
def register(user:User,db:Session = Depends(get_db))-> UserResponce:
    return register_service(user,db)