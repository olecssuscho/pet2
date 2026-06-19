from schemas.dbmodels import PaymentRequestDB,UserDB
from sqlalchemy.orm import Session
from fastapi import status,HTTPException

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
        asker = user.email
    )
    db.add(payment_request_db)
    db.commit()

    return payment_request_db.status
    
def get_payment_requests_services(user:UserDB,db:Session):
    return db.query(PaymentRequestDB).filter((PaymentRequestDB.from_user_id == user.id) | (PaymentRequestDB.to_user_id == user.id)).all()