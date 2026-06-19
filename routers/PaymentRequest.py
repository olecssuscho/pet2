from fastapi import Depends,APIRouter
from schemas.models import PaymentRequestMODEL,UserMODEL
from sqlalchemy.orm import Session
from dependency import get_db,get_current_user
from services.PaymentRequest import payment_request_services,get_payment_requests_services

router = APIRouter()

@router.post("/payment_request")
def payment_request(payment_request: PaymentRequestMODEL,user:UserMODEL = Depends(get_current_user), db:Session = Depends(get_db)):
    return payment_request_services(user,payment_request,db)

@router.get("/payment/get")
def get_payment_requests(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_payment_requests_services(user,db)