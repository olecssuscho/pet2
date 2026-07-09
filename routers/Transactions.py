from schemas.models import TransactionMODEL,UserMODEL
from sqlalchemy.orm import Session
from fastapi_pagination import paginate,Page
from fastapi import Depends,APIRouter, Header,Path,BackgroundTasks,Request
from dependency import get_db,get_current_user
from schemas.responces import TransactionResponceGood
from services.Transactions import (transaction_service,
                                    get_transactions_services,
                                    get_particular_transaction_services,
                                    delete_transaction_services)
from limit import limiter

router = APIRouter(prefix="/transaction", tags=["Transactions"])

@router.post("/transaction")
@limiter.limit("5/minute")
def transaction(request: Request,backgroundtask:BackgroundTasks,transaction:TransactionMODEL,x_idempotency_key:str = Header(None),user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return transaction_service(backgroundtask,user.email,transaction,transaction.reciever_email,db,request)

@router.get("/transaction/get", response_model=Page[TransactionResponceGood])
def get_transactions(user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return paginate(get_transactions_services(user,db))

@router.get("/transaction/{id}")
def get_particular_transaction(id:int = Path(),user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_particular_transaction_services(id,user,db)

@router.delete("/transaction/delete")
def delete_transaction(id:int,user:UserMODEL = Depends(get_current_user),db:Session = Depends(get_db)):
    return delete_transaction_services(id,user,db)
    