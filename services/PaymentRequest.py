from schemas.dbmodels import PaymentRequestDB,UserDB,TransactionDB
from schemas.models import TransactionMODEL
from sqlalchemy.orm import Session
from fastapi import status,HTTPException
from services.Transactions import transaction_service

def payment_request_services(user:UserDB,payment_request:PaymentRequestDB,db:Session):
    
    if db.query(UserDB).filter(UserDB.email == payment_request.to_user_email).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Receiver not found")
    
    if payment_request.amount<0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Sender amount less than 0 ")
    
    to_id = db.query(UserDB).filter(UserDB.email==payment_request.to_user_email).first().id
    payment_request_db = PaymentRequestDB(
        from_user_id = user.id,
        to_user_id = to_id,
        from_user_email = user.email,
        to_user_email = payment_request.to_user_email,
        amount = payment_request.amount,
        message = payment_request.message,
        status = "success",
        asker = user.email,
        type = payment_request.type
    )
    db.add(payment_request_db)
    db.commit()

    return payment_request_db.status
    
def get_payment_requests_services(user:UserDB,db:Session):
    return db.query(PaymentRequestDB).filter((PaymentRequestDB.from_user_id == user.id) | (PaymentRequestDB.to_user_id == user.id)).all()

def payment_request_approve_services(id:int,user:UserDB,db:Session):
    PaymentRequest = db.query(PaymentRequestDB).filter(PaymentRequestDB.id == id).first()
    
    if not PaymentRequest:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    transaction = TransactionMODEL(
        reciever_email = PaymentRequest.to_user_email,
        amount = PaymentRequest.amount,
        status = PaymentRequest.status,
        type = PaymentRequest.type
    )

    transaction_db = transaction_service(user.email,transaction,PaymentRequest.to_user_email,db)

    PaymentRequest.transaction_id = transaction_db.id
    PaymentRequest.status = "success"
    db.commit()
    return PaymentRequest.status
