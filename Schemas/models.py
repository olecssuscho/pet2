from pydantic import BaseModel
from typing import Literal

class UserMODEL(BaseModel):
    email:str
    password:str
    full_name:str
    balance:float

class TransactionMODEL(BaseModel):
    sender_email:str
    reciever_email:str
    amount:float
    status:str = "pending"
    type:Literal["transfer","deposit","refund"]

class PaymentRequestMODEL(BaseModel):
    from_user_id:int
    to_user_id:int
    amount:float
    message:str
    status:str = "pending"

class RefundMODEL(BaseModel):
    transaction_id:int
    reason:str
    status:str = "pending"
