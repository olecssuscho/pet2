from fastapi import Depends,APIRouter
from schemas.models import RefundMODEL,UserMODEL
from sqlalchemy.orm import Session
from dependency import get_db,get_current_user
from services.Refund import refund_services

router = APIRouter(prefix="/refund", tags=["Refunds"])

@router.post("/refund")
def refund(refund:RefundMODEL,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return refund_services(user.email,refund,db)