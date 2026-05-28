from pydantic import BaseModel
from typing import Literal

class User(BaseModel):
    email:str
    password:str
    full_name:str
    balance:float
    is_blocked:bool
    created_at:str

class Transaction(BaseModel):
    sender_id:int
    reciever_id:int
    amount:float
    status:Literal["pending","success","failed","frozen"]="pending"
    type:Literal["transfer","deposit","refund"]

class PaymentRequest(BaseModel):
    from_user_id:int
    to_user_id:int
    amount:float
    message:str
    status:Literal["pending","success","failed","frozen"]="pending"

class Refund(BaseModel):
    transaction_id:int
    reason:str
    status:Literal["pending","success","failed","frozen"]="pending"
