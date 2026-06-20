from pydantic import BaseModel
from typing import Literal

class UserMODEL(BaseModel):
    email:str
    password:str
    full_name:str
    balance:float

class TransactionMODEL(BaseModel):
    reciever_email:str
    amount:float
    status:str = "pending"
    type:Literal["transfer","deposit","refund"]

class PaymentRequestMODEL(BaseModel):
    to_user_email:str
    amount:float
    message:str
    status:str = "pending"
    type:Literal["transfer","deposit","refund"]

class RefundMODEL(BaseModel):
    transaction_id:int
    reason:str
    status:str = "pending"
