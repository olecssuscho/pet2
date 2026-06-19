from schemas.models import TransactionMODEL,UserMODEL
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from dependency import get_db,get_current_user
from services.Transactions import transaction_service

router = APIRouter()

@router.post("/transaction")
def transaction(transaction:TransactionMODEL,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return transaction_service(user.email,transaction,transaction.reciever_email,db)