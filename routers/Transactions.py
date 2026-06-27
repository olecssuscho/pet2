from schemas.models import TransactionMODEL,UserMODEL
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter,Path,BackgroundTasks
from dependency import get_db,get_current_user
from services.Transactions import transaction_service,get_transactions_services,get_particular_transaction_services

router = APIRouter()

@router.post("/transaction")
def transaction(backgroundtask:BackgroundTasks,transaction:TransactionMODEL,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return transaction_service(backgroundtask,user.email,transaction,transaction.reciever_email,db)

@router.get("/transaction/get")
def get_transactions(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_transactions_services(user,db)

@router.get("/transaction/{id}")
def get_particular_transaction(id:int = Path(),user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_particular_transaction_services(id,user,db)
    