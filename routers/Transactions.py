from schemas.models import TransactionMODEL
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from dependency import get_db
from services.Transactions import transaction_service

router = APIRouter()

@router.post("/transaction")
def transaction(transaction:TransactionMODEL,db:Session = Depends(get_db)):
    return transaction_service(transaction,transaction.sender_email,transaction.reciever_email,db)