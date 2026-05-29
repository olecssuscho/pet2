from schemas.dbmodels import Transaction,User
from schemas.responces import TransactionResponceGood
from sqlalchemy.orm import Session
from fastapi import status,HTTPException

def transaction_service(transaction:Transaction,db:Session) -> TransactionResponceGood:
    sender_id = transaction.sender_id
    if not sender_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sender not found")
    sender_db = db.query(User).filter(User.id==sender_id).first()
    if not sender_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Sender unauthorized")
    receiver_id = transaction.reciever_id
    if not receiver_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver not found")
    receiver_db = db.query(User).filter(User.id==receiver_id).first()
    if not receiver_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Receiver unauthorized")
    sender_amount = transaction.amount
    if sender_db.balance<sender_amount:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Sender amount less than 0")
    db.query(User).filter(User.id==sender_id).update({User.balance: User.balance - sender_amount})
    db.query(User).filter(User.id==receiver_id).update({User.balance: User.balance + sender_amount})
    db.commit()
    return transaction
    