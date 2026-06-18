from fastapi import Depends,APIRouter
from schemas.models import RefundMODEL
from sqlalchemy.orm import Session
from dependency import get_db
from services.Refund import refund_services

router = APIRouter()

@router.post("/refund")
def refund(refund:RefundMODEL,db:Session = Depends(get_db)):
    return refund_services(refund,db)