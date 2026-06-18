from fastapi import Depends,APIRouter
from schemas.models import PaymentRequestMODEL
from sqlalchemy.orm import Session
from dependency import get_db
from services.PaymentRequest import payment_request_services

router = APIRouter()

@router.post("/payment_request")
def payment_request(payment_request: PaymentRequestMODEL, db:Session = Depends(get_db)):
    return payment_request_services(payment_request,db)